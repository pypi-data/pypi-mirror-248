"""AnyscaleTaskRunner."""
import os
import sys
from contextlib import AsyncExitStack
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urlparse

from anyscale import AnyscaleSDK
from anyscale.sdk.anyscale_client.models import ClustersQuery, TerminateClusterOptions, TextQuery
from prefect_ray import RayTaskRunner
from pydantic.v1.utils import deep_update

from . import named_anyscale_compute_config


class AnyscaleTaskRunner(RayTaskRunner):  # type: ignore
    """Drop in replacement for RayTaskRunner with sensible default settings."""

    def __init__(self, address: Optional[str] = None, **init_kwargs: Any):
        if not os.getenv("ANYSCALE_CLUSTER_ENV") and not init_kwargs.get("cluster_env"):
            sys.exit(
                "No cluster_env provided. Please specify one via ANYSCALE_CLUSTER_ENV or the cluster_env init arg."
            )
        default_address = (
            f"{os.environ.get('RAY_ADDRESS', 'anyscale://anonymous-one-off-cluster')}-"
            f"{datetime.now().strftime('%Y-%m-%dT%H-%M-%S-%f')}"
        )
        default_init_kwargs = {
            "cluster_compute": named_anyscale_compute_config.default_compute_config(),
            "runtime_env": {"working_dir": str(os.getenv("ANYSCALE_WORKING_DIR", "./"))},
            "autosuspend": -1,
        }

        super().__init__(
            address or default_address,
            deep_update(default_init_kwargs, init_kwargs or {}),
        )

        self.logger.warning(
            "The AnyscaleTaskRunner is deprecated."
            "Please use RayTasksRunner instead and rely on the anyscale_config flow parameter to specify infrastructure."
        )

    def terminate_cluster(self) -> None:
        """Terminate Anyscale cluster.

        Parse Ray address and call Anyscale SDK to terminate the cluster.
        """
        parsed_address = urlparse(self.address)
        cluster_name = parsed_address.path if parsed_address.path else parsed_address.netloc
        cluster_response = AnyscaleSDK().search_clusters(ClustersQuery(name=TextQuery(equals=cluster_name)))
        try:
            cluster_id = cluster_response.results[0].id
            self.logger.info(f"Terminating {cluster_name}.")
            AnyscaleSDK().terminate_cluster(cluster_id, TerminateClusterOptions())
        except IndexError:
            self.logger.error(f"Cluster {cluster_name} not found. Cannot terminate.")

    async def _start(self, exit_stack: AsyncExitStack) -> None:
        """Start Anyscale Task Runner.

        Add terminate_cluster callback to exit stack before starting the RayTaskRunner.
        This invokes the callback after all resources from the RayTaskRunner have been released.
        """
        exit_stack.callback(self.terminate_cluster)
        await super()._start(exit_stack)
