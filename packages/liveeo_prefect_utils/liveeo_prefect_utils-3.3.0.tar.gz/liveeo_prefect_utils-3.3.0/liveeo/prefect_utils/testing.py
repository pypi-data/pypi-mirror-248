"""Helper functions and fixtures for Prefect Flow tests."""

from itertools import chain
from typing import Any, Dict, List, Union

import pytest
from prefect.logging.loggers import disable_run_logger
from prefect.server import models
from prefect.server.database.dependencies import provide_database_interface
from prefect.server.schemas.core import Constant, Parameter, TaskRun, TaskRunResult
from prefect.server.schemas.filters import FlowFilter, FlowRunFilter, FlowRunFilterId
from prefect.server.schemas.sorting import FlowRunSort, TaskRunSort
from prefect.testing.utilities import prefect_test_harness
from prefect.utilities.asyncutils import sync_compatible
from pytest import FixtureRequest


@pytest.fixture(autouse=True, scope="session")
def prefect_test_fixture() -> Any:
    """Replace Orion Cloud with in memory DB and disable run logger."""
    with prefect_test_harness(), disable_run_logger():
        yield


@pytest.fixture(scope="function")
def run_flow(request: FixtureRequest) -> Dict[str, Any]:
    """Forward input parameter, execute flow and retrieve flow graph.

    This fixture can be parameterized indirectly with a param dictionary.
    This dictionary is expected to contain:
        "flow"  : a prefect @flow decorated function
        "args"  : optional list of args as input for the flow
        "kwargs": optional dict of kwargs as input for the flow

    Example usage:

        @pytest.mark.parametrize(
        "run_flow",
        [
            {"flow": my_flow, "args": [0, 1], "kwargs": {"a": 0, "b": 1}},
            {"flow": my_flow_2, "args": [0, 1]},
            {"flow": my_flow_3, "kwargs": {"a": 0, "b": 1}},
            {"flow": my_flow_3},
        ],
        indirect=True,
        )

    Args:
        request: pytest FixtureRequest containing param values from indirect parametrization.

    Returns
    -------
        Dict: containing all inputs (flow, args, kwargs), result of executed flow function and a flow_graph (a list of dependent TaskRuns)
    """
    return {
        **request.param,
        "result": request.param["flow"](*request.param.get("args", []), **request.param.get("kwargs", {})),
        "flow_graph": read_latest_flow_run_task_runs(request.param["flow"].name),
    }


@sync_compatible
async def read_latest_flow_run_task_runs(flow_name: str) -> Any:
    """Query Orion for tasks runs of the latest flow run by name.

    Args:
        flow_name: filter criteria for flow runs

    Returns
    -------
        a list of dicts representing task runs ordered by end time
    """
    db_interface = provide_database_interface()
    async with db_interface.session_context(begin_transaction=True) as session:
        latest_flow_run = (
            await models.flow_runs.read_flow_runs(
                session=session,
                db=db_interface,
                flow_filter=FlowFilter(name={"any_": [flow_name]}),
                sort=FlowRunSort.END_TIME_DESC,
                limit=1,
            )
        )[0]

        task_runs = await models.task_runs.read_task_runs(
            session=session,
            db=db_interface,
            flow_run_filter=FlowRunFilter(id=FlowRunFilterId(any_=[latest_flow_run.id])),
            sort=TaskRunSort.END_TIME_DESC,
        )

        return task_runs[::-1]


def upstream_dependencies(
    task_run: TaskRun,
) -> List[Union[TaskRunResult, Parameter, Constant]]:
    """Merge dependencies from all task inputs."""
    return list(set(chain(*task_run.task_inputs.values())))
