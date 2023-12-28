"""AnyscaleJob Prefect Worker."""

import os
import sys
import time
from datetime import datetime
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Type, cast

import anyio.abc
from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.exceptions import ApiException
from anyscale.sdk.anyscale_client.models.cluster_environments_query import ClusterEnvironmentsQuery
from anyscale.sdk.anyscale_client.models.create_cluster_compute_config import CreateClusterComputeConfig
from anyscale.sdk.anyscale_client.models.create_production_job import CreateProductionJob
from anyscale.sdk.anyscale_client.models.create_production_job_config import CreateProductionJobConfig
from anyscale.sdk.anyscale_client.models.ha_job_states import HaJobStates
from anyscale.sdk.anyscale_client.models.projects_query import ProjectsQuery
from anyscale.sdk.anyscale_client.models.text_query import TextQuery
from anyscale.util import get_endpoint
from prefect import get_client
from prefect.client.cloud import get_cloud_client
from prefect.exceptions import InfrastructureNotAvailable, InfrastructureNotFound
from prefect.utilities.asyncutils import run_sync_in_worker_thread
from prefect.utilities.pydantic import JsonPatch
from prefect.workers.base import BaseJobConfiguration, BaseVariables, BaseWorker, BaseWorkerResult
from pydantic import BaseModel, ConfigDict, Field, create_model, field_validator
from pydantic.v1.utils import deep_update
from typing_extensions import Literal

from liveeo.prefect_utils.anyscale import named_anyscale_compute_config

if TYPE_CHECKING:
    from prefect.client.schemas.objects import FlowRun
    from prefect.client.schemas.responses import DeploymentResponse
    from prefect.logging.loggers import PrefectLogAdapter

# anyscale overwrites stdout and stderr to support fancy terminal spinners
# prefect does not like that, so we reset them here
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

MAX_UPTIME_DEV = 1440
MAX_UPTIME_PRD = 10080


def opinionated_anyscale_config(
    allowed_named_default_configs: Optional[List[Callable[..., Any]]] = None
) -> Type[BaseModel]:
    """Create anyscale config model with limited set of named default configs."""
    if allowed_named_default_configs:
        named_default_config_values = tuple(fn.__name__ for fn in allowed_named_default_configs)
    else:
        named_default_config_values = tuple(
            fn_name
            for fn_name in dir(named_anyscale_compute_config)
            if not fn_name.startswith("__") and fn_name.endswith("compute_config")
        )

    @field_validator("compute_config_customization")
    def _must_be_json_patch(value: Any) -> Any:
        if value:
            JsonPatch(value)
        return value

    timeout = None
    if os.environ.get("PREFECT_WORKSPACE") == "dev":
        timeout = MAX_UPTIME_DEV
    elif os.environ.get("PREFECT_WORKSPACE") == "prd":
        timeout = MAX_UPTIME_PRD

    return create_model(
        "AnyscaleConfig",
        __base__=BaseModel,
        __pydantic_validators__={"_must_be_json_patch": _must_be_json_patch},
        model_config=ConfigDict(extra="forbid"),
        named_default_config=(
            Optional[Literal[named_default_config_values]],
            Field(
                title="Compute config name",
                description="Infrastructure configuration that suits the flows use case.",
                default="default_compute_config",
            ),
        ),
        compute_config_customization=(
            Optional[List[Dict[str, Any]]],
            Field(
                title="Compute config customization",
                description="Compute config customization as JsonPatch. "
                "Specify 'null' or '[]' for no customization. "
                "Warning: you are entering advanced mode.",
                default=None,
            ),
        ),
        contract_uuid=(
            Optional[str],
            Field(
                title="Contract UUID",
                description="Tag that will be propagated to EC2 instances.",
                default="research_and_development",
            ),
        ),
        timeout=(
            Optional[int],
            Field(
                title="Timeout",
                description="Maximum cluster uptime in minutes (-1: no timeout).",
                default=timeout,
            ),
        ),
    )


def prefect_runtime_environment_hook(runtime_env: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Set working_dir to local directory."""
    if not runtime_env:
        runtime_env = {}

    # If no working_dir is specified, we use the current
    # directory as the working directory -- this will be
    # the directory containing the source code which is
    # downloaded by the Prefect engine.
    if not runtime_env.get("working_dir"):
        runtime_env["working_dir"] = "."

    return runtime_env


class AnyscaleJobWorkerConfiguration(BaseJobConfiguration):  # type: ignore
    """
    Configuration class used by the Anyscale Job worker.

    An instance of this class is passed to the Anyscale Job worker's `run` method
    for each flow run. It contains all the information necessary to execute
    the flow run as an Anyscale job.

    Attributes
    ----------
        anyscale_cluster_env: Anyscale cluster env to use for the execution of the job.
        job_watch_timeout_seconds: The number of seconds to wait for the job to
            complete before timing out. If `None`, the worker will wait indefinitely.
        prefect_api_key_aws_secret: The name and region of the AWS secret containing the Prefect API key.
    """

    anyscale_cluster_env: str = Field()
    job_watch_timeout_seconds: Optional[int] = Field(default=None)


class AnyscaleJobWorkerVariables(BaseVariables):  # type: ignore
    """
    Default variables for the Anyscale Job worker.

    The schema for this class is used to populate the `variables` section of the default
    base job template.
    """

    anyscale_cluster_env: str = Field(description="Cluster environment to use for the execution of the job.")
    job_watch_timeout_seconds: Optional[int] = Field(
        description=(
            "Number of seconds to wait for each event emitted by a job before "
            "timing out. If not set, the worker will wait for each event indefinitely."
        ),
        default=None,
    )


class AnyscaleJobWorkerResult(BaseWorkerResult):  # type: ignore
    """Contains information about the final state of a completed Anyscale Job."""


class AnyscaleJobWorker(BaseWorker):  # type: ignore
    """Prefect worker that executes flow runs within Anyscale Jobs."""

    type = "anyscale-job"
    job_configuration = AnyscaleJobWorkerConfiguration
    job_configuration_variables = AnyscaleJobWorkerVariables
    _description = "Execute flow runs within Anyscale Jobs. Requires Anyscale Cloud."
    _display_name = "Anyscale Job"
    _documentation_url = None
    _logo_url = "https://docs.anyscale.com/site-assets/logo.png"  # noqa

    async def run(
        self,
        flow_run: "FlowRun",
        configuration: AnyscaleJobWorkerConfiguration,
        task_status: Optional[anyio.abc.TaskStatus] = None,
    ) -> AnyscaleJobWorkerResult:
        """
        Execute a flow run within an Anyscale Job and wait for the flow run to complete.

        Args:
            flow_run: The flow run to execute
            configuration: The configuration to use when executing the flow run.
            task_status: The task status object for the current flow run. If provided,
                the task will be marked as started.

        Returns
        -------
            AnyscaleWorkerResult: A result object containing information about the
                final state of the flow run
        """
        async with get_client() as client:
            deployment = await client.read_deployment(flow_run.deployment_id)

        async with get_cloud_client() as client:
            workspace_handle = (await client.read_workspaces())[0].workspace_handle

        anyscale_config = self._get_anyscale_config(flow_run, deployment)
        compute_config = self._get_compute_config(flow_run, workspace_handle, anyscale_config)

        (_, job_id) = self._submit_anyscale_job(flow_run, workspace_handle, configuration, compute_config)

        await self._update_flow_run_tags(
            flow_run, self._fixed_run_tags(flow_run, job_id, anyscale_config.contract_uuid, deployment.version)
        )

        # Indicate that the job has started
        if task_status is not None:
            task_status.started(job_id)

        status_code = await run_sync_in_worker_thread(
            self._watch_job, job_id, flow_run, configuration.job_watch_timeout_seconds
        )

        return AnyscaleJobWorkerResult(identifier=job_id, status_code=status_code)

    def _fixed_run_tags(
        self, flow_run: "FlowRun", job_id: str, contract_uuid: str, deployment_version: str
    ) -> List[str]:
        return [
            f"contract_uuid:{contract_uuid}",
            f"job_id:{job_id}",
            f"deployment_id:{flow_run.deployment_id}",
            f"deployment_version:{deployment_version}",
            f"creator:{flow_run.created_by.display_value}",
        ]

    # Add tags to the flow run
    async def _update_flow_run_tags(self, flow_run: "FlowRun", run_tags: List[str]) -> None:
        async with get_client() as client:
            await client.update_flow_run(
                flow_run_id=str(flow_run.id),
                tags=set(flow_run.tags).union(set(run_tags)),
            )

    @staticmethod
    def _get_api_key(logger: "PrefectLogAdapter") -> str:
        aws_secret_id = os.environ.get("ANYSCALE_PREFECT_AWS_SECRET_ID", None)
        aws_region = os.environ.get("ANYSCALE_PREFECT_AWS_REGION", None)
        if aws_secret_id and aws_region:
            api_key = (
                f"`aws secretsmanager get-secret-value "
                f"--secret-id {aws_secret_id} "
                f"--region {aws_region} "
                f"--output=text "
                f"--query=SecretString`"
            )
        else:
            api_key = os.environ["PREFECT_API_KEY"]
            logger.warning(
                "Your PREFECT_API_KEY is currently stored in plain text. "
                "Consider using a secret manager to store your secrets."
            )
        return api_key

    def _submit_anyscale_job(
        self,
        flow_run: "FlowRun",
        workspace_handle: str,
        configuration: AnyscaleJobWorkerConfiguration,
        compute_config: Dict[str, Any],
    ) -> Tuple[str, str]:
        logger = self.get_flow_run_logger(flow_run)

        configuration.command = f"PREFECT_API_KEY={self._get_api_key(logger)} " f"{configuration.command}"

        job_name = f"prefect-job-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')}-{flow_run.id}"

        sdk = AnyscaleSDK()

        cluster_env_id = (
            sdk.search_cluster_environments(
                cluster_environments_query=ClusterEnvironmentsQuery(
                    name=TextQuery(equals=configuration.anyscale_cluster_env)
                )
            )
            .results[0]
            .id
        )
        cluster_env_build_id = (
            sdk.list_cluster_environment_builds(cluster_environment_id=cluster_env_id, desc=True, count=1)
            .results[0]
            .id
        )

        configuration.env.pop("PREFECT_API_KEY", None)
        configuration.env[
            "RAY_RUNTIME_ENV_HOOK"
        ] = "liveeo.prefect_utils.anyscale.infrastructure.prefect_runtime_environment_hook"

        job_config = CreateProductionJobConfig(
            entrypoint=configuration.command,
            build_id=cluster_env_build_id,
            compute_config=CreateClusterComputeConfig(**compute_config),
            runtime_env={"env_vars": configuration.env},
            max_retries=0,
        )

        project_id = (
            sdk.search_projects(ProjectsQuery(name=TextQuery(equals=f"prefect-{workspace_handle}"))).results[0].id
        )
        create_production_job = CreateProductionJob(
            name=job_name,
            project_id=project_id,
            config=job_config,
        )

        logger.debug(f"Submitting Anyscale Job {job_name} with configuration:")
        logger.debug(f"{create_production_job.to_dict()}")

        job_id = sdk.create_job(create_production_job=create_production_job).result.id

        logger.info(
            "The two datadoghq.eu links below relate to a project in beta testing phase, please ask DataOps for more information"
        )

        logger.info(
            (
                "Find head node logs at "
                f"https://app.datadoghq.eu/logs?query=source%3Avector%20node%3Ahead%20%40anyscale_prodjob_id%3A{job_id}"
                "%20&cols=host%2Cservice&index=%2A&messageDisplay=inline&refresh_mode=sliding&stream_sort=desc&view=spans&viz=stream&live=true"
            )
        )
        logger.info(
            (
                "Find worker node logs at "
                f"https://app.datadoghq.eu/logs?query=source%3Avector%20node%3Aworker%20%40anyscale_prodjob_id%3A{job_id}"
                "%20&cols=host%2Cservice&index=%2A&messageDisplay=inline&refresh_mode=sliding&stream_sort=desc&view=spans&viz=stream&live=true"
            )
        )

        logger.info(f'View the job in the UI at {get_endpoint(f"/jobs/{job_id}")}.')

        return job_name, job_id

    def _get_compute_config(self, flow_run: "FlowRun", workspace_handle: str, anyscale_config: Any) -> Dict[str, Any]:
        named_default_config = cast(Optional[str], anyscale_config.named_default_config)
        if named_default_config:
            compute_config = cast(
                Dict[str, Any],
                getattr(named_anyscale_compute_config, named_default_config)(),
            )
        else:
            compute_config = named_anyscale_compute_config.default_compute_config()

        # in order to be backwards compatible with flows that were created before the timeout was introduced
        # we need to set the correct timeout if it is None
        # consequently, None cannot be used to unset the timeout, which is why we use -1 for that
        if anyscale_config.timeout is None:
            timeout = MAX_UPTIME_DEV if workspace_handle == "dev" else MAX_UPTIME_PRD
            compute_config = JsonPatch([{"op": "add", "path": "/maximum_uptime_minutes", "value": timeout}]).apply(
                compute_config
            )
        elif anyscale_config.timeout == -1:
            compute_config = JsonPatch([{"op": "remove", "path": "/maximum_uptime_minutes"}]).apply(compute_config)
        else:
            compute_config = JsonPatch(
                [{"op": "add", "path": "/maximum_uptime_minutes", "value": anyscale_config.timeout}]
            ).apply(compute_config)

        if anyscale_config.compute_config_customization:
            compute_config = JsonPatch(anyscale_config.compute_config_customization).apply(compute_config)

        cost_allocation_tags = {
            "contract_uuid": anyscale_config.contract_uuid,
            "prefect_flow_run_id": str(flow_run.id),
            "prefect_flow_name": flow_run.name,
        }
        compute_config = self._update_tags(compute_config, cost_allocation_tags)

        return compute_config

    @staticmethod
    def _update_tags(compute_config: Dict[str, Any], update_tags: Dict[str, Any]) -> Dict[str, Any]:
        if not update_tags:
            # no tags to update - return original comput config
            return compute_config

        if "TagSpecifications" in compute_config["aws_advanced_configurations_json"]:
            # if tags are specified in customization
            for tag_spec in compute_config["aws_advanced_configurations_json"]["TagSpecifications"]:
                if tag_spec["ResourceType"] == "instance":
                    # update and extend customization tags with tags from parameter
                    customization_tags: Dict[str, str] = {tag["Key"]: tag["Value"] for tag in tag_spec["Tags"]}
                    tags = cast(Dict[str, str], deep_update(customization_tags, update_tags))
                    tag_spec["Tags"] = [{"Key": key, "Value": value} for key, value in tags.items()]
                    return compute_config

            # if no parameter tags found, add them to customization
            compute_config["aws_advanced_configurations_json"]["TagSpecifications"].append(
                {
                    "ResourceType": "instance",
                    "Tags": [{"Key": key, "Value": value} for key, value in update_tags.items()],
                }
            )
            return compute_config

        # pylint: disable=duplicate-code
        # if no tags were specified in customization at all, update aws_advanced_configurations_json
        tag_customization = {
            "aws_advanced_configurations_json": {
                "TagSpecifications": [
                    {
                        "ResourceType": "instance",
                        "Tags": [{"Key": key, "Value": value} for key, value in update_tags.items()],
                    },
                ]
            }
        }
        return cast(Dict[str, Any], deep_update(compute_config, tag_customization))

    @staticmethod
    def _get_anyscale_config(flow_run: "FlowRun", deployment: "DeploymentResponse") -> Any:
        """Get anyscale config.

        Assembling it from:
        1. Deployment or default parameters
        2. Flow parameters
        """
        anyscale_config = opinionated_anyscale_config()().model_dump(mode="json")

        deployment_parameters = deployment.parameter_openapi_schema["properties"]
        if (
            "anyscale_config" in deployment_parameters
            and "default" in deployment_parameters["anyscale_config"]
            and deployment_parameters["anyscale_config"]["default"]
        ):
            # config from deployment default parameters
            anyscale_config = deployment_parameters["anyscale_config"]["default"]

        if "anyscale_config" in flow_run.parameters and flow_run.parameters["anyscale_config"]:
            # config from submitted flow parameters
            flow_config = flow_run.parameters["anyscale_config"]

            for key in anyscale_config:
                if key in flow_config:
                    anyscale_config[key] = flow_config[key]

        return opinionated_anyscale_config()(**anyscale_config)

    def _log_service_urls(
        self, sdk: AnyscaleSDK, cluster_id: str, log_services_urls: Dict[str, str], flow_run: "FlowRun"
    ) -> None:
        services_urls = sdk.get_cluster(cluster_id).result.services_urls
        for url_name, url_id in list(log_services_urls.items()):
            url = getattr(services_urls, url_id)
            if url:
                self.get_flow_run_logger(flow_run).info(f"View the cluster {url_name} in the UI: {url}")
                del log_services_urls[url_name]

    def _watch_job(
        self, job_id: str, flow_run: "FlowRun", job_watch_timeout_seconds: int, polling_delay: int = 30
    ) -> int:
        start = time.time()

        wait_states = [
            HaJobStates.PENDING,
            HaJobStates.AWAITING_CLUSTER_START,
            HaJobStates.UPDATING,
            HaJobStates.RUNNING,
            HaJobStates.CLEANING_UP,
            HaJobStates.RESTARTING,
        ]
        success_states = [HaJobStates.SUCCESS]
        fail_states = [
            HaJobStates.ERRORED,
            HaJobStates.TERMINATED,
            HaJobStates.BROKEN,
            HaJobStates.OUT_OF_RETRIES,
        ]

        sdk = AnyscaleSDK()
        # list of service URLs to be logged to the flow run
        log_services_urls = {
            "Ray dashboard": "ray_dashboard_url",
            "Grafana dashboard": "metrics_dashboard_url",
            # "Non-running Grafana dashboard": "persistent_metrics_url",
            # "Jupyter Notebook": "jupyter_notebook_url",
            # "Webterminal": "webterminal_auth_url",
        }
        logger = self.get_flow_run_logger(flow_run)

        while True:
            prod_job = sdk.get_production_job(production_job_id=job_id).result
            current_state = prod_job.state.current_state

            if current_state not in [*wait_states, *success_states, *fail_states]:
                logger.warning(f"Found Anyscale Job {prod_job.name} in unexpected state {current_state}!")

            if prod_job.state.cluster_id and log_services_urls:
                self._log_service_urls(sdk, prod_job.state.cluster_id, log_services_urls, flow_run)

            if current_state in success_states:
                return 0

            if current_state in fail_states:
                logger.warning(f"Infrastructure failed with state: {current_state}")
                return 1

            if job_watch_timeout_seconds and time.time() - start > job_watch_timeout_seconds:
                logger.warning(
                    f"Prefect agent job watch timeout ({job_watch_timeout_seconds}s) exceeded. "
                    f"Infrastructure might continue to run."
                )
                return 1

            time.sleep(polling_delay)

    async def kill_infrastructure(
        self, infrastructure_pid: str, configuration: AnyscaleJobWorkerConfiguration, grace_seconds: int = 30
    ) -> None:
        """Stop a job for a cancelled flow run based on the provided infrastructure PID and run configuration."""
        try:
            AnyscaleSDK().terminate_job(production_job_id=infrastructure_pid)
        except ApiException as api_exception:
            if api_exception.status == "404":
                raise InfrastructureNotFound(api_exception.reason) from api_exception

            raise InfrastructureNotAvailable(api_exception.reason) from api_exception
