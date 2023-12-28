"""Configure fixtures for tests."""
from pathlib import Path

import pytest
from _pytest.logging import LogCaptureFixture
from loguru import logger


@pytest.fixture()  # type: ignore[misc]
def test_file(tmp_path: Path) -> Path:
    """
    Create a temporary file and return its Path.

    Parameters
    ----------
    tmp_path : Path
        Temporary path in which to create a file.

    Returns
    -------
    Path
        Returns path to a test file.
    """
    _file = tmp_path / "test.txt"
    _file.touch()
    return _file


@pytest.fixture()  # type: ignore[misc]
def test_jpg() -> Path:
    """
    Return path to a sample JPG image.

    Returns
    -------
    Path
        Path to a sample jpg file.
    """
    return Path("tests/resources/sample.jpg")


@pytest.fixture()  # type: ignore[misc]
def test_no_exif_jpg() -> Path:
    """
    Return path to a sample JPG image.

    Returns
    -------
    Path
        Path to a sample jpg file.
    """
    return Path("tests/resources/no_exif.jpg")


@pytest.fixture()  # type: ignore[misc]
def caplog(caplog: LogCaptureFixture) -> LogCaptureFixture:  # pylint: disable=redefined-outer-name
    """Caplog fixture to work with loguru.

    See https://loguru.readthedocs.io/en/latest/resources/migration.html#replacing-caplog-fixture-from-pytest-library
    """
    handler_id = logger.add(
        caplog.handler,
        format="{message}",
        level=0,
        filter=lambda record: record["level"].no >= caplog.handler.level,
        enqueue=False,  # Set to 'True' if your test is spawning child processes.
    )
    yield caplog
    logger.remove(handler_id)
