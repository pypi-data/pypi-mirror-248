"""Utility methods to retrieve information about the current environment."""

from typing import List
from uuid import UUID

import prefect.client.cloud
from prefect.client.schemas import Workspace
from prefect.settings import PREFECT_API_URL
from prefect.utilities.asyncutils import sync_compatible


@sync_compatible
async def _read_prefect_workspaces() -> List[Workspace]:
    """Read the details for the locally configured workspaces."""
    async with prefect.client.cloud.get_cloud_client() as client:
        workspaces: List[Workspace] = await client.read_workspaces()
    return workspaces


def retrieve_prefect_workspace_handle() -> str:
    """Retrieve the Prefect workspace handle from the Prefect API.

    Returns
    -------
        Prefect workspace handle as string, e.g., "dev", "prd"
    """
    # Check if Prefect API URL setting is set and has the expected pattern:
    # https://api.prefect.cloud/api/accounts/$UUID_ACCOUNT/workspaces/$UUID_WORKSPACE
    if not PREFECT_API_URL.value():
        raise ValueError("Prefect API URL is not set.")
    if PREFECT_API_URL.value().split("/")[-2] != "workspaces":
        raise ValueError("Prefect API URL has not the expected pattern (workspace).")
    if PREFECT_API_URL.value().split("/")[-4] != "accounts":
        raise ValueError("Prefect API URL has not the expected pattern (account).")

    # Extract account and workspace UUIDs from Prefect API URL setting.
    prefect_account_uuid = UUID(PREFECT_API_URL.value().split("/")[-3])
    prefect_workspace_uuid = UUID(PREFECT_API_URL.value().split("/")[-1])

    # Get list of locally configured workspaces, outsourced to not get the async virus
    workspaces = _read_prefect_workspaces()

    # Find and return the workspace with the matching account and workspace UUIDs.
    for workspace in workspaces:
        if workspace.account_id == prefect_account_uuid and workspace.workspace_id == prefect_workspace_uuid:
            return str(workspace.workspace_handle)

    raise ValueError("Prefect workspace handle could not be retrieved.")
