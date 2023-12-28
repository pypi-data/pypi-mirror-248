"""Classes and functions that help us cache Prefect task results."""

import copy
import os
import warnings
from typing import Any, Dict, Optional
from urllib.parse import urlparse

import boto3
import botocore
from prefect.context import TaskRunContext
from prefect.filesystems import LocalFileSystem
from prefect.results import ResultStorage, get_default_result_storage
from prefect.utilities.hashing import hash_objects


def _get_s3_object_summary(s3_path: str) -> Any:
    """Retrieve the S3 ObjectSummary for a given S3 path (s3://bucket/key/k/e.y)."""
    s3_url = urlparse(s3_path, allow_fragments=False)
    s3_bucket = s3_url.netloc
    s3_key = s3_url.path.lstrip("/")

    try:
        s3_resource = boto3.resource("s3")
        s3_resource.Object(s3_bucket, s3_key).load()  # head request: check if file exists
        return s3_resource.ObjectSummary(s3_bucket, s3_key)
    except botocore.exceptions.ClientError:
        return None


def get_result_cache_filesystem() -> ResultStorage:
    """Get a Prefect WritableFileSystem for storing Prefect task results."""
    warnings.warn(
        "This function is deprecated and will be removed in future versions. Prefect-Pipeline already takes care of "
        "this with the PREFECT_DEFAULT_RESULT_STORAGE_BLOCK environment variable.",
        DeprecationWarning,
    )

    # env var for s3 storage block is injected during docker image build
    if os.environ.get("PREFECT_RESULT_CACHE") is not None:
        return f"s3/{os.environ.get('PREFECT_RESULT_CACHE')}"

    # no env var set -> use prefect default path for local storage
    return get_default_result_storage()


def liveeo_task_input_hash(context: "TaskRunContext", arguments: Dict[str, Any]) -> Optional[str]:
    """
    Task cache key function that takes LiveEOs setup/infrastructure into account.

    A task cache key implementation which hashes all inputs to the task using a JSON or
    cloudpickle serializer. If any arguments are not JSON serializable, the pickle
    serializer is used as a fallback. If cloudpickle fails, this will return a null key
    indicating that a cache key could not be generated for the given inputs.

    Arguments:
        context: the active `TaskRunContext`
        arguments: a dictionary of arguments to be passed to the underlying task

    Returns
    -------
        a string hash if hashing succeeded, else `None`
    """
    # We use the result storage location to distinguish execution environments.
    storage_location = context.result_factory.storage_block_id
    # If executed locally, a new storage block is created for each run -> use path instead of UUID
    if isinstance(context.result_factory.storage_block, LocalFileSystem):
        # Use the abspath to be able to differentiate relative paths
        storage_location = os.path.abspath(context.result_factory.storage_block.basepath)

    return hash_objects(  # type: ignore
        # We use the task key to get the qualified name for the task and include the
        # task functions `co_code` bytes to avoid caching when the underlying function changes
        context.task.task_key,
        context.task.fn.__code__.co_code.hex(),
        # arguments passed to the task
        arguments,
        # storage location
        storage_location,
    )


def liveeo_task_input_hash_s3(context: "TaskRunContext", arguments: Dict[str, Any]) -> Optional[str]:
    """
    Task cache key function that adds the etag checksum for each S3 path before using the default hash function.

    A task cache key implementation which hashes all inputs to the task using a JSON or
    cloudpickle serializer. If any arguments are not JSON serializable, the pickle
    serializer is used as a fallback. If cloudpickle fails, this will return a null key
    indicating that a cache key could not be generated for the given inputs.

    Arguments:
        context: the active `TaskRunContext`
        arguments: a dictionary of arguments to be passed to the underlying task

    Returns
    -------
        a string hash if hashing succeeded, else `None`
    """
    enhanced_arguments = copy.deepcopy(arguments)
    for key in arguments:
        if isinstance(arguments[key], str) and arguments[key].startswith("s3://"):
            object_summary = _get_s3_object_summary(arguments[key])
            if object_summary is not None:
                enhanced_arguments.update({key + "-e_tag": object_summary.e_tag})
    return liveeo_task_input_hash(context, enhanced_arguments)


def liveeo_task_input_hash_s3_modified(context: "TaskRunContext", arguments: Dict[str, Any]) -> Optional[str]:
    """
    Task cache key function that adds the last modified ts for each S3 path before using the default hash function.

    A task cache key implementation which hashes all inputs to the task using a JSON or
    cloudpickle serializer. If any arguments are not JSON serializable, the pickle
    serializer is used as a fallback. If cloudpickle fails, this will return a null key
    indicating that a cache key could not be generated for the given inputs.

    Arguments:
        context: the active `TaskRunContext`
        arguments: a dictionary of arguments to be passed to the underlying task

    Returns
    -------
        a string hash if hashing succeeded, else `None`
    """
    enhanced_arguments = copy.deepcopy(arguments)
    for key in arguments:
        if isinstance(arguments[key], str) and arguments[key].startswith("s3://"):
            object_summary = _get_s3_object_summary(arguments[key])
            if object_summary is not None:
                enhanced_arguments.update({key + "-last_modified": object_summary.last_modified})
    return liveeo_task_input_hash(context, enhanced_arguments)
