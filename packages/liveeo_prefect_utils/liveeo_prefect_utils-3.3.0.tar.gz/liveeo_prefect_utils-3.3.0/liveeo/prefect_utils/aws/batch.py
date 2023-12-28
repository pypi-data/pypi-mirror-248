"""AWS Batch helper functions."""

import asyncio
import json
import logging
import random
import re
import threading  # needed by threadlocals pylint: disable=unused-import
from datetime import datetime
from functools import partial
from pathlib import Path
from typing import IO, Any, Awaitable, Callable, Dict, List, Optional, Tuple, Union

import anyio
from aiobotocore.session import get_session
from aiobotocore.waiter import WaiterModel, create_waiter_with_client
from prefect import get_run_logger
from prefect.context import get_run_context
from pydantic import BaseModel, Extra

# we use our own waiter definition so that we can meddle with the poll timing
_default_waiter_definition = {
    "version": 2,
    "waiters": {
        "JobComplete": {
            "delay": 120,
            "operation": "DescribeJobs",
            "maxAttempts": 5040,
            "description": "Wait until job status is SUCCEEDED or FAILED",
            "acceptors": [
                {
                    "argument": "jobs[].status",
                    "expected": "SUCCEEDED",
                    "matcher": "pathAll",
                    "state": "success",
                },
                {
                    "argument": "jobs[].status",
                    "expected": "FAILED",
                    "matcher": "pathAny",
                    "state": "success",
                },
            ],
        }
    },
}


def _update_dict(original: Dict[Any, Any], updates: Dict[Any, Any]) -> Dict[Any, Any]:
    """Merge dicts recursively. borrowed from airflow_pipelines/src/utils.py."""
    updated = original.copy()
    for key, node in updates.items():
        if isinstance(node, dict):
            updated[key] = _update_dict(updated.get(key, {}), node)
        else:
            updated[key] = node
    return updated


def _run_async_from_sync(__fn: Callable[..., Awaitable[Any]], *args: Any, **kwargs: Any) -> Any:
    """Call async methods from sync code."""
    call = partial(__fn, *args, **kwargs)

    try:
        anyio.from_thread.threadlocals.current_async_module
    except AttributeError:
        # we are in the main thread: just run the method
        return anyio.run(call)

    # we are in an async worker thread: run it in main thread's
    # event loop, blocking the worker thread until completion
    return anyio.from_thread.run(call)


class BatchException(Exception):
    """Generic exception for unsuccessful Batch jobs."""


class BatchRetryException(BatchException):
    """Special exception failed Batch jobs due to EC2 SPOT instance termination."""


class BatchParameters(BaseModel, extra=Extra.forbid):
    """AWS Batch job configuration parameters."""

    module: str
    version: str
    region_name: str
    job_queue: str
    timeout: int
    memory: int
    vcpu: int
    tags: List[str]


class BatchJob:  # pylint: disable=too-many-instance-attributes
    """Easily start AWS Batch jobs from Prefect @tasks.

    Args:
    ----
        client_kwargs: Passed to the Boto3 create client call.
            Most useful for specifying the region_name.
        submit_job_kwargs: The default values for a submitting a batch job.
        waiter_definition: Optional waiter definition.
        raise_errors: raise error on Batch job failure. Default true.
        spot_retry: number of times to automagically retry spot instance
            failures. Defaults to 3.
        verbose: Log job_id and results to the Prefect logger. Default true.
        get_logs: Get the logs messages from cloudwatch after job completion
            and add to the results. Also logged to the prefect logs
            when verbose is true. Default true.

    """

    def __init__(
        self,
        *,
        client_kwargs: Optional[Dict[str, Any]] = None,
        submit_job_kwargs: Optional[Dict[str, Any]] = None,
        waiter_definition: Optional[Dict[str, Any]] = None,
        raise_errors: bool = True,
        spot_retry: int = 3,
        verbose: bool = True,
        get_logs: bool = True,
    ):
        self.client_kwargs = client_kwargs if client_kwargs else {}
        self.submit_job_kwargs = submit_job_kwargs if submit_job_kwargs else {}
        self.waiter_definition = waiter_definition if waiter_definition else _default_waiter_definition
        self.raise_errors = raise_errors
        self.spot_retry = spot_retry
        self.verbose = verbose
        self.get_logs = get_logs
        self.boto_session = get_session()

    @classmethod
    async def run_async(
        cls, *, job_name: Optional[str] = None, cmd: List[str], batch_parameters: BatchParameters, **kwargs: Any
    ) -> Tuple[str, Dict[str, Any]]:
        """Create an BatchJob object and run a batch job immediately. Async version.

        Args:
        ----
            job_name: Passed to the actual submit_job call. Defaults to
                the Prefect task_run_name.
            cmd: Batch job command.
            batch_parameters: Batch job parameters used to setup the batch client and passed to the submit call.
            **kwargs: Any other arguments that will be passed on to the BatchJob constructor.s
        """
        client_kwargs = _update_dict({"region_name": batch_parameters.region_name}, kwargs.get("client_kwargs", {}))
        kwargs.pop("client_kwargs", None)

        job_definition_name = BatchJobDefinitionsHelper.module_name_to_job(batch_parameters.module)
        job_definition_revision = await BatchJobDefinitionsHelper.get_job_definition_revision_async(
            batch_parameters.region_name, batch_parameters.module, batch_parameters.version
        )
        job_definition = f"{job_definition_name}:{job_definition_revision}"
        submit_job_kwargs = _update_dict(
            {
                "containerOverrides": {
                    "command": cmd,
                    "resourceRequirements": [
                        {"type": "MEMORY", "value": f"{batch_parameters.memory}"},
                        {"type": "VCPU", "value": f"{batch_parameters.vcpu}"},
                    ],
                },
                "timeout": {"attemptDurationSeconds": batch_parameters.timeout},
                "jobQueue": batch_parameters.job_queue,
                "jobDefinition": job_definition,
                "tags": {tag: "" for tag in batch_parameters.tags},
            },
            kwargs.get("submit_job_kwargs", {}),
        )

        kwargs.pop("submit_job_kwargs", None)

        batch_job = cls(client_kwargs=client_kwargs, submit_job_kwargs=submit_job_kwargs, **kwargs)

        return await batch_job.batch_job_async(jobName=job_name)

    @classmethod
    def run(
        cls, *, job_name: Optional[str] = None, cmd: List[str], batch_parameters: BatchParameters, **kwargs: Any
    ) -> Tuple[str, Dict[str, Any]]:
        """Create an BatchJob object and run a batch job immediately.

        Synchronous wrapper around the async version. (See above).
        """
        kwargs["job_name"] = job_name
        kwargs["cmd"] = cmd
        kwargs["batch_parameters"] = batch_parameters
        return _run_async_from_sync(cls.run_async, **kwargs)  # type: ignore

    async def batch_job_async(self, *, jobName: Optional[str] = None, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        """
        Create an AWS Batch job and wait for completion. Async version.

        Args:
        ----
            jobName: Passed to the actual submit_job call. Defaults to
                the Prefect task_run_name.
            **kwargs: custom waiter_definition and any other arguments get recursively merged with the default
                 submit_job_kwargs from the BatchJob object (overriding those)
                 and then passed on to the Boto3 submit_job call.

        :raises BatchRetryException: after failing self.spot_retry times.
        """
        logger = get_run_logger()
        if jobName is None:
            ctx = get_run_context()
            jobName = ctx.task_run.name

        tries = 1
        while tries < self.spot_retry:
            try:
                return await self._batch_job_async(logger=logger, jobName=jobName, **kwargs)
            except BatchRetryException as retry_exception:
                exception = retry_exception
                tries += 1
                if self.verbose:
                    logger.info(f"retrying batch job for {jobName}")
                continue
        # fall through, retried too many times, reraise exception
        raise exception from None

    def batch_job(self, **kwargs: Any) -> Tuple[str, Dict[str, Any]]:
        """
        Create a AWS Batch job and wait for completion.

        Synchronous wrapper around the async version. (See above).
        """
        return _run_async_from_sync(self.batch_job_async, **kwargs)  # type: ignore

    async def _batch_job_async(
        self,
        *,
        logger: logging.Logger,
        jobName: str,
        waiter_definition: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> Tuple[str, Dict[str, Any]]:
        waiter_definition = waiter_definition or self.waiter_definition

        submit_job_kwargs = _update_dict(self.submit_job_kwargs, kwargs)

        async with self.boto_session.create_client("batch", **self.client_kwargs) as batch:
            # delay batch job submission by random delay < waiter delay
            # this spreads out Batch API requests over time when submitting a large number of jobs simultaneously.
            await asyncio.sleep(random.random() * waiter_definition["waiters"]["JobComplete"]["delay"])
            response = await batch.submit_job(jobName=jobName, **submit_job_kwargs)

            job_id = response["jobId"]
            if self.verbose:
                logger.debug(f"{jobName}: batch job_id {job_id}")

            waiter_model = WaiterModel(waiter_definition)
            waiter_name = "JobComplete"
            waiter = create_waiter_with_client(waiter_name, waiter_model, batch)

            if self.verbose:
                aws_region_name = self.client_kwargs["region_name"]
                logger.info(
                    f"https://{aws_region_name}.console.aws.amazon.com/batch/home"
                    f"?region={aws_region_name}#jobs/detail/{job_id}"
                )

            await waiter.wait(
                jobs=[job_id],
            )

            response = await batch.describe_jobs(jobs=[job_id])

        # logger.debug(f"response = {response}")
        job_response = response["jobs"][0]  # only interested in the last attempt
        job_info = {k: job_response.get(k) for k in ["status", "statusReason", "createdAt", "startedAt", "stoppedAt"]}
        if job_response["attempts"]:
            job_info.update(
                {k: job_response["attempts"][-1]["container"].get(k) for k in ["exitCode", "logStreamName", "reason"]}
            )

            if self.get_logs:
                job_info["messages"] = await self._get_logs(
                    logger=logger,
                    logStreamName=job_info["logStreamName"],
                )

        if self.verbose:
            logger.debug(f"{jobName} batch job_id {job_id}: {job_info}")

        # detect spot instance termination
        if job_info["status"] == "FAILED":
            if self.spot_retry and re.match(r"Host EC2.*terminated", job_info["statusReason"]):
                raise BatchRetryException(job_info)
            if self.raise_errors:
                raise BatchException(job_info)

        return job_id, job_info

    async def _get_logs(self, *, logger: logging.Logger, logStreamName: str) -> List[str]:
        async with self.boto_session.create_client("logs", **self.client_kwargs) as logs_client:
            # cloudwatch logs aren't available immediately, wait 60s first
            await asyncio.sleep(60)

            # this will get the latest 1 megabyte or 10k events, whichever is less
            response = await logs_client.get_log_events(
                logGroupName="/aws/batch/job",
                logStreamName=logStreamName,
            )

        messages = []
        for event in response["events"]:
            # TODO: set correct timezome. now it's in utc # pylint: disable=fixme
            timestamp = datetime.fromtimestamp(event["timestamp"] / 1000.0).isoformat(sep=" ", timespec="milliseconds")
            # TODO: return tuple instead of string. # pylint: disable=fixme
            msg = f"{timestamp} {event['message']}"
            messages.append(msg)

        if self.verbose:
            for msg in messages:
                logger.info(msg)

        return messages


class BatchJobDefinitionsHelper:
    """Helper functions to retrieve batch job definition names and revisions.

    adapted from liveeo_prefect_1_utils.
    """

    @classmethod
    async def get_job_definition_revision_async(cls, aws_region: str, module_name: str, version: str) -> Optional[str]:
        """Get corresponding job definition for a module and version. Async version."""
        revisions_list = await cls.get_revisions_from_aws_batch(module_name, aws_region)
        return cls.get_matching_revision(version, revisions_list)

    @classmethod
    def get_job_definitions_revisions(
        cls,
        **kwargs: Any,
    ) -> Dict[str, str]:
        """Sync wrapper for get_job_definition_revision_async."""
        return _run_async_from_sync(cls.get_job_definitions_revisions_async, **kwargs)  # type: ignore

    @classmethod
    async def get_job_definitions_revisions_async(
        cls,
        aws_region: str,
        module_versions_file: Union[IO[str], Path],
        export_path: Optional[Path] = None,
    ) -> Dict[str, str]:
        """Get list of batch job definition names and revisions from a modules and versions file/stream."""
        modules_revisions = {}
        # TODO: use a try block here. # pylint: disable=fixme
        if isinstance(module_versions_file, Path):
            with open(module_versions_file, "r", encoding="utf-8") as file:
                modules_dict = json.load(file)
        else:
            modules_dict = json.load(module_versions_file)

        for module_name, version in modules_dict.items():
            modules_revisions[
                module_name
            ] = f"{cls.module_name_to_job(module_name)}:{await cls.get_job_definition_revision_async(aws_region, module_name, version)}"

        if export_path:
            # create cached revisions file
            with open(export_path, "w", encoding="utf-8") as export_file:
                json.dump(modules_revisions, export_file, indent=2)

        return modules_revisions

    @staticmethod
    def module_name_to_job(module_name: str) -> str:
        """Convert module name to job name according to convention."""
        return f"{module_name}-job"

    @staticmethod
    async def get_revisions_from_aws_batch(module: str, aws_region: str) -> List[Tuple[str, str]]:
        """Retrieve list of available batch job revisions for a module."""
        job_name = BatchJobDefinitionsHelper.module_name_to_job(module)
        revisions_list = []
        # client = boto3.client("batch", region_name=aws_region)
        boto_session = get_session()
        async with boto_session.create_client("batch", region_name=aws_region) as batch:
            pages = batch.get_paginator("describe_job_definitions").paginate(
                jobDefinitionName=job_name, status="ACTIVE"
            )

            revisions = [
                (job["revision"], job["containerProperties"]["image"])
                async for page in pages
                for job in page["jobDefinitions"]
            ]
            revisions_list += revisions

        return revisions_list

    @staticmethod
    def get_matching_revision(version: str, revisions_list: List[Tuple[str, str]]) -> Optional[str]:
        """Get latest batch job revision that matches a module version from a list of revisions."""
        # the list comes pre-ordered with newest revisions first,
        # so there's no need to order the list to get the latest that matches
        for revision, docker_image in revisions_list:
            if version in docker_image:
                return revision
        return None
