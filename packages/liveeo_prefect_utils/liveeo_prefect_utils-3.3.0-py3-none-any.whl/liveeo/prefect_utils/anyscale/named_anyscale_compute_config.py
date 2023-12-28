"""Named Default configs for all common use cases."""
from typing import Any, Dict

from pydantic.v1.utils import deep_update

from liveeo.prefect_utils.anyscale.compute_config import ComputeConfig, WorkerNode


def head_only_compute_config(**kwargs: Any) -> Dict[str, Any]:
    """Liveeo ready to use config for cluster with one head node only."""
    return ComputeConfig(tasks_on_head_node=True, **kwargs).config


def default_compute_config(**kwargs: Any) -> Dict[str, Any]:
    """Liveeo ready to use config for general purpose."""
    return (
        ComputeConfig(**kwargs)
        .add_worker_node(WorkerNode(name="worker-node-m6i-xlarge", instance_type="m6i.xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-m6a-xlarge", instance_type="m6a.xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-m6i-2xlarge", instance_type="m6i.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-m6a-2xlarge", instance_type="m6a.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-m6i-4xlarge", instance_type="m6i.4xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-m6a-4xlarge", instance_type="m6a.4xlarge"))
        .config
    )


def compute_optimized_compute_config(**kwargs: Any) -> Dict[str, Any]:
    """Liveeo ready to use config for compute heavy workloads."""
    return (
        ComputeConfig(**kwargs)
        .add_worker_node(WorkerNode(name="worker-node-c6i-2xlarge", instance_type="c6i.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6a-2xlarge", instance_type="c6a.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6i-4xlarge", instance_type="c6i.4xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6a-4xlarge", instance_type="c6a.4xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6i-12xlarge", instance_type="c6i.12xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6a-12xlarge", instance_type="c6a.12xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6i-24xlarge", instance_type="c6i.24xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-c6a-24xlarge", instance_type="c6a.24xlarge"))
        .config
    )


def memory_optimized_compute_config(**kwargs: Any) -> Dict[str, Any]:
    """Liveeo ready to use config for memory heavy workloads."""
    # current default cloud has not r instance types in zone 1a
    az_customization = {"allowed_azs": ["eu-central-1b", "eu-central-1c"]}
    customization = deep_update(az_customization, kwargs.pop("customization", {}))

    return (
        ComputeConfig(customization=customization, **kwargs)
        .add_worker_node(WorkerNode(name="worker-node-r6i-2xlarge", instance_type="r6i.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-r6a-2xlarge", instance_type="r6a.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-r6i-4xlarge", instance_type="r6i.4xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-r6a-4xlarge", instance_type="r6a.4xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-r6i-8xlarge", instance_type="r6i.8xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-r6a-8xlarge", instance_type="r6a.8xlarge"))
        .config
    )


def gpu_optimized_compute_config(**kwargs: Any) -> Dict[str, Any]:
    """Liveeo ready to use config for gpu workloads."""
    return (
        ComputeConfig(**kwargs)
        .add_worker_node(WorkerNode(name="worker-node-g5-2xlarge", instance_type="g5.2xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-g5-4xlarge", instance_type="g5.4xlarge"))
        .add_worker_node(WorkerNode(name="worker-node-g5-8xlarge", instance_type="g5.8xlarge"))
        .config
    )
