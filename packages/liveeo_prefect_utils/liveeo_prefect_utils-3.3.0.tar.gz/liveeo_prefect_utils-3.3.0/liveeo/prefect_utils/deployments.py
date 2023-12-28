"""Utility functions for working with Prefect deployments."""

from typing import Any, List, Optional, Union

from anyio import move_on_after, sleep
from prefect.client.orchestration import get_client
from prefect.client.schemas import FlowRun
from prefect.client.schemas.filters import FlowRunFilter
from prefect.utilities.asyncutils import sync_compatible


@sync_compatible
async def wait(
    *flow_runs: FlowRun, polling_interval: int = 30, timeout: Optional[float] = None
) -> Union[List[FlowRun], FlowRun]:
    """Wait for flow run or flow runs to finish.

    Args:
    ----
        *flow_runs (FlowRun): Single or multiple flow runs to wait for.
        polling_interval (int, optional): Polling interval in seconds. Defaults to 30.
        timeout (float, optional): Timeout in seconds. Defaults to None - waiting forever.

    Returns
    -------
        Union[List[FlowRun], FlowRun]: List of flow runs if multiple flow runs were passed, otherwise a single flow run.

    Usage:
    -----

    ```python
    from prefect_utils.deployments import wait
    from prefect.deployments import run_deployment

    flow_run_1 = run_deployment(name="Awesome Flow/test_flow", parameters={"param": "this is flow 1"}, timeout=0)

    completed_flow_run = wait(flow_run_1)
    ```

    OR:
    ```python
    flow_run_1 = run_deployment(name="Awesome Flow/test_flow", parameters={"param": "this is flow 1"}, timeout=0)
    flow_run_2 = run_deployment(name="Awesome Flow/test_flow", parameters={"param": "this is flow 2"}, timeout=0)

    (completed_flow_run_1, completed_flow_run_2) = wait(flow_run_1, flow_run_2)
    ```
    """
    flow_runs_response = await _wait(*flow_runs, polling_interval=polling_interval, timeout=timeout)

    return flow_runs_response[0] if len(flow_runs_response) == 1 else flow_runs_response


async def _wait(*flow_runs: FlowRun, polling_interval: int = 30, timeout: Optional[float] = None) -> List[FlowRun]:
    """Wait for flow run or flow runs to finish.

    Private implementation that always returns list of flow runs.
    """
    if all((flow_run_response.state.is_final() for flow_run_response in flow_runs)):
        return list(flow_runs)

    client = get_client()

    flow_run_filter = FlowRunFilter(id={"any_": [flow_run.id for flow_run in flow_runs]})

    flow_runs_response: List[FlowRun] = await client.read_flow_runs(flow_run_filter=flow_run_filter)
    with move_on_after(timeout):
        while not all((flow_run_response.state.is_final() for flow_run_response in flow_runs_response)):
            await sleep(polling_interval)
            flow_runs_response = await client.read_flow_runs(flow_run_filter=flow_run_filter)

    # API cannot sort by list of ids, so we sort the response manually
    flow_runs_response.sort(key=lambda i: [flow_run.id for flow_run in flow_runs].index(i.id))

    if len(flow_runs_response) != len(flow_runs):
        raise ValueError(
            f"Could not find all flow runs. Found flow runs {[flow_run.id for flow_run in flow_runs_response]}, but expected {[flow_run.id for flow_run in flow_runs]}."
        )

    return flow_runs_response


@sync_compatible
async def result(
    *flow_runs: FlowRun, raise_on_failure: bool = True, polling_interval: int = 30, timeout: Optional[float] = None
) -> Union[List[Any], Any]:
    """Wait for flow run or flow runs to finish and return result.

    Args:
    ----
        *flow_runs (FlowRun): Single or multiple flow runs to wait for.
        raise_on_failure (bool, optional): Raise exception if flow run or flow runs failed. Defaults to False.
        polling_interval (int, optional): Polling interval in seconds. Defaults to 30.
        timeout (float, optional): Timeout in seconds. Defaults to None - waiting forever.

    Returns
    -------
        Union[List[Any], Any]: List of results if multiple flow runs were passed, otherwise a single result.

    Usage:
    -----

    ```python
    from prefect_utils.deployments import result
    from prefect.deployments import run_deployment

    flow_run_1 = run_deployment(name="Awesome Flow/test_flow", parameters={"param": "this is flow 1"}, timeout=0)

    flow_run_result = result(flow_run_1)
    ```

    OR:
    ```python
    flow_run_1 = run_deployment(name="Awesome Flow/test_flow", parameters={"param": "this is flow 1"}, timeout=0)
    flow_run_2 = run_deployment(name="Awesome Flow/test_flow", parameters={"param": "this is flow 2"}, timeout=0)

    (flow_run_result_1, flow_run_result_2) = result(flow_run_1, flow_run_2)
    ```
    """
    final_flow_run_or_flow_runs = await _wait(*flow_runs, polling_interval=polling_interval, timeout=timeout)

    results = [
        await flow_run.state.result(fetch=True, raise_on_failure=raise_on_failure)
        for flow_run in final_flow_run_or_flow_runs
    ]

    return results[0] if len(results) == 1 else results
