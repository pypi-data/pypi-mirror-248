"""Configure fixtures for tests."""
from pathlib import Path

import pytest


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
