"""Anyscale compute config helper functions.

This module offers functionality to conveniently create Anyscale compute configs with sensible defaults,
while still enabling fully custom configuration.

LiveEO maintained default configs:
    - default_compute_config: Compute config with multiple general purpose instances
    - head_only_compute_config: Head-only config with one general purpose instance
    - compute_optimized_compute_config: Compute optimized config
    - memory_optimized_compute_config: Memory optimized config
    - gpu_optimized_compute_config: GPU optimized config

To facilitate switching anyscale clouds and setting tags on instances, all default configs can be parameterized
with a cloud_id and a tags dict that is applied to all instance in the cluster (tags provided via the dedicated parameter
take precedence over tags provided via the customization parameter).

Usage examples:
Default config:
@flow(
    name="my-flow",
    task_runner=RayTaskRunner(
        address=address,
        init_kwargs={
            "cluster_env": cluster_env,
            "cluster_compute": default_compute_config(),
        }
    )
)

Memory optimized config with tags:
@flow(
    name="my-flow",
    task_runner=RayTaskRunner(
        address=address,
        init_kwargs={
            "cluster_env": cluster_env,
            "cluster_compute":  memory_optimized_compute_config(tags={"purpose": "tagging"}),
        }
    )
)

Custom config:
@flow(
    name="my-flow",
    task_runner=RayTaskRunner(
        address=address,
        init_kwargs={
            "cluster_env": cluster_env,
            "cluster_compute": ComputeConfig(
                head_node_instance_type="m5.2xlarge",
                customization={
                    "head_node_type": {
                        "aws_advanced_configurations_json": {
                            "BlockDeviceMappings": [
                                {
                                    "DeviceName": "/dev/sda1",
                                    "Ebs": {
                                        "DeleteOnTermination": True,
                                        "Iops": 15000,
                                        "Throughput": 1000,
                                        "VolumeSize": 600,
                                        "VolumeType": "gp3",
                                    },
                                }
                            ],
                        }
                    }
                },
            )
            .add_worker_node(WorkerNode(name="my-node", instance_type="t2.small"))
            .add_worker_node(
                WorkerNode(
                    name="my-node",
                    instance_type="t2.medium",
                    customization={"resources": {"custom_resources": {"db_token": 3}}},
                )
            )
            .config,
        }
    )
)
"""

from __future__ import annotations

from typing import Any, Dict, Optional, cast

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models import CloudsQuery, TextQuery
from pydantic.v1.utils import deep_update


class WorkerNode:
    """Worker node helper class."""

    def __init__(
        self,
        *,
        name: str,
        instance_type: str,
        max_workers: int = 10,
        min_workers: int = 0,
        use_spot: bool = True,
        fallback_to_ondemand: bool = True,
        customization: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.config: Dict[str, Any] = {
            "name": name,
            "instance_type": instance_type,
            "max_workers": max_workers,
            "min_workers": min_workers,
            "fallback_to_ondemand": fallback_to_ondemand,
            "use_spot": use_spot,
        }
        if customization:
            self.config = deep_update(self.config, customization)


class ComputeConfig:
    """Compute config helper class."""

    def __init__(
        self,
        *,
        cloud_id: Optional[str] = None,
        cloud_name: Optional[str] = None,
        head_node_instance_type: str = "m6i.xlarge",
        tags: Optional[Dict[str, str]] = None,
        customization: Optional[Dict[str, Any]] = None,
        tasks_on_head_node: bool = False,
    ) -> None:
        if cloud_name and cloud_id:
            raise ValueError("You can only pass one parameter: cloud_id or cloud_name.")

        if cloud_name and not cloud_id:
            cloud_id = self.get_anyscale_cloud_id_from_cloud_name(cloud_name=cloud_name)

        if not cloud_id and not cloud_name:
            cloud_id = self.get_default_anyscale_cloud_id()

        if not cloud_name and cloud_id:
            pass

        # pylint: disable=duplicate-code
        self.config: Dict[str, Any] = {
            "cloud_id": cloud_id,
            "head_node_type": {
                "instance_type": head_node_instance_type,
                "name": "head-node",
            },
            "maximum_uptime_minutes": 10080,  # 7 days
            "region": "eu-central-1",
            "worker_node_types": [],
            "aws_advanced_configurations_json": {
                "TagSpecifications": [
                    {"ResourceType": "instance", "Tags": [{"Key": "as-feature-multi-zone", "Value": "true"}]}
                ]
            },
        }

        if not tasks_on_head_node:
            self.config["head_node_type"]["resources"] = {"cpu": 0}

        if customization:
            self.config = deep_update(self.config, customization)

        if tags:
            # Tags from the tags parameter take precedence over tags provided via the customization
            if "TagSpecifications" in self.config["aws_advanced_configurations_json"]:
                # if tags are specified in customization
                for tag_spec in self.config["aws_advanced_configurations_json"]["TagSpecifications"]:
                    if tag_spec["ResourceType"] == "instance":
                        # update and extend customization tags with tags from parameter
                        customization_tags: Dict[str, str] = {tag["Key"]: tag["Value"] for tag in tag_spec["Tags"]}
                        tags = cast(Dict[str, str], deep_update(customization_tags, tags))
                        tag_spec["Tags"] = [{"Key": key, "Value": value} for key, value in tags.items()]
                        break
            else:
                # if no tags were specified in customization, update aws_advanced_configurations_json
                tag_customization = {
                    "aws_advanced_configurations_json": {
                        "TagSpecifications": [
                            {
                                "ResourceType": "instance",
                                "Tags": [{"Key": key, "Value": value} for key, value in tags.items()],
                            },
                        ]
                    }
                }
                self.config = deep_update(self.config, tag_customization)

    def add_worker_node(self, worker_node: WorkerNode) -> ComputeConfig:
        """Add worker node to compute config."""
        self.config["worker_node_types"].append(worker_node.config)
        return self

    @staticmethod
    def get_default_anyscale_cloud_id() -> Any:
        """Retrieve the default anyscale cloud id."""
        sdk = AnyscaleSDK()

        anyscale_default_cloud_id = sdk.get_default_cloud().result.id

        return anyscale_default_cloud_id

    @staticmethod
    def get_anyscale_cloud_id_from_cloud_name(cloud_name: str) -> Any:
        """Retrieve anyscale cloud id using the anyscale cloud name."""
        try:
            sdk = AnyscaleSDK()
            anyscale_cloud_info = sdk.search_clouds(CloudsQuery(name=TextQuery(equals=cloud_name)))

            return anyscale_cloud_info.results[0].id

        except Exception as exc:
            raise NameError("The passed cloud name does not exist in the anyscale environment.") from exc
