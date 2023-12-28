"""Tests for mvdate."""
import logging
from collections.abc import Callable
from datetime import datetime
from pathlib import Path

import PIL
import pytest

from mvdate import mvdate

# Get current date time
current_datetime = datetime.now()

# pylint: disable=protected-access


@pytest.mark.parametrize(
    ("base", "ext", "n_matches"), [("./mvdate/", "py", 3), ("./tests/resources", "jpg", 2)]
)  # type: ignore[misc]
def test_find(base: str, ext: str, n_matches: int) -> None:
    """Test files are found correctly."""
    files_found = list(mvdate.find(base, ext))
    assert len(files_found) == n_matches


@pytest.mark.skip(  # type: ignore[misc]
    reason="Need to figure out how to get a fixed ctime for a file in a clone repo."
)
@pytest.mark.parametrize(  # type: ignore[misc]
    ("test_file", "creation"), [("tests/resources/fixed_date_time", 1697919000.0)]
)
def test_get_file_date(test_file: str, creation: float) -> None:
    """Test extraction of file date."""
    assert mvdate.get_file_date(Path(test_file)) == creation


@pytest.mark.parametrize(("method"), [("ctime"), ("mtime")])  # type: ignore[misc]
def test__get_file_date(method: str) -> None:
    """Test private _get_file_date() returns a callable object."""
    assert isinstance(mvdate._get_file_date(method), Callable)  # type: ignore[arg-type]


def test__get_file_date_unsupported_method() -> None:
    """Test raising ValueError when unsupported method provided."""
    with pytest.raises(ValueError, match="Invalid method provided : not a method"):
        assert mvdate._get_file_date("not a method")  # type: ignore[truthy-function]


@pytest.mark.skip(  # type: ignore[misc]
    reason="Need to figure out how to get a fixed ctime for a file in a cloned repo."
)
@pytest.mark.parametrize(  # type: ignore[misc]
    ("test_file", "creation"), [("tests/resources/fixed_date_time", 1697919000.0)]
)
def test_file_date_ctime(test_file: str, creation: float) -> None:
    """Test extraction of file ctime."""
    assert mvdate._file_date_ctime(Path(test_file)) == creation


@pytest.mark.skip(  # type: ignore[misc]
    reason="Need to figure out how to get a fixed mtime for a file in a cloned repo."
)
@pytest.mark.parametrize(  # type: ignore[misc]
    ("test_file", "creation"), [("tests/resources/fixed_date_time", 1697919000.0)]
)
def test_file_date_mtime(test_file: str, creation: float) -> None:
    """Test extraction of file mtime."""
    assert mvdate._file_date_mtime(Path(test_file)) == creation


def test_file_date_exif(test_jpg: Path) -> None:
    """Test extraction of file exif."""
    assert mvdate._file_date_exif(test_jpg) == 1699196740.0


def test_file_date_exif_typeerror() -> None:
    """Check _file_date_exif() raises a FileNotFoundError if it doesn't get a reference to a file."""
    with pytest.raises(FileNotFoundError):
        assert mvdate._file_date_exif(Path("not_a_file"))


def test_file_date_exif_keyerror(test_no_exif_jpg: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Check _file_date_exif() logs a warning that there is no Exif date if missing from a file."""
    with caplog.at_level(logging.WARNING):
        print(f"{caplog.text=}")
        mvdate._file_date_exif(test_no_exif_jpg)
        assert "No Exif data, using ctime for file : " in caplog.text


@pytest.mark.parametrize(  # type: ignore[misc]
    ("date_time", "target_dir"),
    [
        ("2023/12/01", "./"),
        ("2023/12/02", "./test/nested"),
        ("2023/12/03", "../test"),
        ("2023/12/04", "../test/nested/parent"),
        ("2023-12-05", "./"),
    ],
)
def test_create_target_dir(date_time: str, target_dir: str, tmp_path: Path) -> None:
    """Test target directory is created."""
    mvdate.create_target_dir(date_time, destination=tmp_path / target_dir)
    check_dir = tmp_path / target_dir / date_time
    assert check_dir.is_dir()


@pytest.mark.parametrize(  # type: ignore[misc]
    ("nesting", "sep", "target_dir"),
    [
        ("Y", False, f"{current_datetime.strftime('%Y')}"),
        ("m", False, f"{current_datetime.strftime('%Y/%m')}"),
        ("d", False, f"{current_datetime.strftime('%Y/%m/%d')}"),
        ("H", False, f"{current_datetime.strftime('%Y/%m/%d/%H')}"),
        ("M", False, f"{current_datetime.strftime('%Y/%m/%d/%H/%M')}"),
        ("M", True, f"{current_datetime.strftime('%Y-%m-%d-%H-%M')}"),
        (None, False, f"{current_datetime.strftime('%Y/%m/%d')}"),
        (None, True, f"{current_datetime.strftime('%Y-%m-%d')}"),
    ],
)
def test_construct_date_time(test_file: Path, nesting: str, sep: bool, target_dir: str) -> None:
    """Test construction of date/time to string."""
    creation_date = mvdate.get_file_date(test_file, method="ctime")
    assert mvdate.construct_date_time(creation_date, nesting, sep) == target_dir


def tests_construct_date_time_raise_unidentified_image_error(test_file: Path) -> None:
    """Test error is raised when file is not an image and therefore has no Exif data."""
    with pytest.raises(PIL.UnidentifiedImageError):
        mvdate.get_file_date(test_file, method="exif")


@pytest.mark.parametrize(  # type: ignore[misc]
    ("nesting", "sep", "date_time"),
    [
        ("Y", False, f"{current_datetime.strftime('%Y')}"),
        ("m", False, f"{current_datetime.strftime('%Y/%m')}"),
        ("d", False, f"{current_datetime.strftime('%Y/%m/%d')}"),
        ("H", False, f"{current_datetime.strftime('%Y/%m/%d/%H')}"),
        ("M", False, f"{current_datetime.strftime('%Y/%m/%d/%H/%M')}"),
        ("M", True, f"{current_datetime.strftime('%Y-%m-%d-%H-%M')}"),
        (None, False, f"{current_datetime.strftime('%Y/%m/%d')}"),
        (None, True, f"{current_datetime.strftime('%Y-%m-%d')}"),
    ],
)
def test_create_file_parent(test_file: Path, nesting: str, sep: bool, date_time: str, tmp_path: Path) -> None:
    """Integration test to check extraction of creation date, deriving target directory and creation work together."""
    creation_date = mvdate.get_file_date(test_file, method="ctime")
    nested_dir = mvdate.construct_date_time(creation_date, nesting, sep)
    mvdate.create_target_dir(date_time, tmp_path)
    print(f"{Path(tmp_path / nested_dir)}")
    assert Path(tmp_path / nested_dir).is_dir()


# Remove temporary file, no more tests use it
Path("tests/resources/test.txt").unlink(missing_ok=True)


@pytest.mark.parametrize(  # type: ignore[misc]
    ("source", "destination", "exception"),
    [
        (Path("test/resource/does_not_exist.txt"), "does_not_exist.txt", FileNotFoundError),
        (Path("test/resource/test.txt"), "somewhere/test.txt", FileNotFoundError),
    ],
)
def test_move_file_errors(source: Path, destination: Path, exception: Exception, tmp_path: Path) -> None:
    """Test FileNotFoundError raised when either source or target file/directory do not exist."""
    with pytest.raises(exception):
        assert mvdate.move_file(source, tmp_path / destination)  # type: ignore[truthy-bool]


def test_move_file(tmp_path: Path) -> None:
    """Test move_file() function."""
    test_file = tmp_path / "test_file.txt"
    test_file.touch()
    destination = tmp_path / "nested"
    destination.mkdir()
    target_file = mvdate.move_file(test_file, destination)
    assert target_file.is_file()


# https://stackoverflow.com/a/76977976/1444043
# @pytest.mark.parametrize(
#     ("args"),
#     [
#         ([f"-b ./", "-e jpg", "-d ./dest", "-m exif", "-n Y"]),
#     ],
# )
# def test_entry_point(args: list, tmp_path: Path) -> None:
#     """Integration test for the main() function."""
#     args = [re.sub(r"./", f"{tmp_path}/", x) for x in args]
#     print(f"[test] args")
#     print(list(tmp_path.rglob(f"**/*.txt")))
#     print(f"[test] tmp_path.is_dir() : {tmp_path.is_dir()}")
#     assert tmp_path.is_dir()
#     destination = Path(tmp_path / "dest")
#     destination.mkdir()
#     print(f"[test] tmp_path.is_dir() : {tmp_path.is_dir()}")
#     assert destination.is_dir()
#     mvdate.main(args=args)
#     moved_files = list(destination.rglob("**/*.jpg"))
#     print(f"@@@@ moved_files : {moved_files}")
#     assert len(moved_files) == 10


@pytest.mark.parametrize(  # type: ignore[misc]
    ("args"),
    [
        (["-v"]),
        (["--version"]),
    ],
)
def test_entry_point_reports_version(args: list, capsys: pytest.LogCaptureFixture) -> None:  # type: ignore[type-arg]
    """Check the version is reported."""
    try:
        mvdate.main(args=args)  # type: ignore[arg-type]
    except SystemExit:
        pass
    assert "Installed version of mvdate" in capsys.readouterr().out
