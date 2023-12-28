"""Helper functions for prefect logging."""

from prefect import get_run_logger


def enable_loguru_support() -> None:
    """Redirect loguru logging messages to the prefect run logger.

    This function should be called from within a Prefect task before calling any module that uses loguru.
    This function can be safely called multiple times.


    Example Usage:

    from prefect import task
    from loguru import loguru_logger
    from liveeo_prefect_utils.logging import enable_loguru_support

    @task()
    def my_task():
        loguru_logger.info("This is hidden from the Prefect UI")
        enable_loguru_support()
        loguru_logger.info("This shows up in the Prefect UI")

    """
    # import here for distributed execution because loguru cannot be pickled.
    from loguru import logger as loguru_logger  # pylint: disable=import-outside-toplevel

    run_logger = get_run_logger()
    loguru_logger.remove()
    log_format = "{name}:{function}:{line} - {message}"
    loguru_logger.add(
        run_logger.debug,
        filter=lambda record: record["level"].name == "DEBUG",
        level="TRACE",
        format=log_format,
    )
    loguru_logger.add(
        run_logger.warning,
        filter=lambda record: record["level"].name == "WARNING",
        level="TRACE",
        format=log_format,
    )
    loguru_logger.add(
        run_logger.error,
        filter=lambda record: record["level"].name == "ERROR",
        level="TRACE",
        format=log_format,
    )
    loguru_logger.add(
        run_logger.critical,
        filter=lambda record: record["level"].name == "CRITICAL",
        level="TRACE",
        format=log_format,
    )
    loguru_logger.add(
        run_logger.info,
        filter=lambda record: record["level"].name not in ["DEBUG", "WARNING", "ERROR", "CRITICAL"],
        level="TRACE",
        format=log_format,
    )
