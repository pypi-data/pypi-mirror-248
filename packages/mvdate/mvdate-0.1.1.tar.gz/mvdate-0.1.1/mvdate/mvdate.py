"""Move files based on date."""
from __future__ import annotations

import argparse as arg
import shutil
import sys
import time
import typing
from datetime import datetime
from pathlib import Path

from PIL import Image
from loguru import logger
from pyfiglet import Figlet
from tqdm import tqdm

from mvdate import __version__

# Copyright 2023 Neil Shephard
#
# This file is part of mvdate.
#
# mvdate is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, version 3 of the License.
#
#
# mvdate is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with mvdate. If not, see
# <https://www.gnu.org/licenses/>.

logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<8}</level> | <level>{message}</level>",
)
logger.add(
    sys.stderr,
    level="ERROR",
    format="<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> | <level>{level:<8}</level> | <level>{message}</level>",
)


def create_parser() -> arg.ArgumentParser:
    """
    Create a parser for reading options.

    Returns
    -------
    arg.ArgumentParser
        Returns an argument parser.
    """
    parser = arg.ArgumentParser(description="Move files to directory structure based on files date.")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Installed version of mvdate : {__version__}",
        help="Report the current installed version of mvdate.",
    )
    parser.add_argument("-e", "--ext", dest="ext", required=False, default="jpg", help="File extension to search for.")
    parser.add_argument(
        "-b",
        "--base",
        dest="base",
        type=str,
        required=False,
        default="./",
        help="Base directory to search for files with extension type. Default './",
    )
    parser.add_argument(
        "-d",
        "--destination",
        dest="dest",
        type=str,
        required=False,
        default="./",
        help="Destination directory to   move files to. Default './",
    )
    parser.add_argument(
        "-l", "--log_file", dest="log_file", type=str, required=False, default=None, help="File to log output to."
    )
    parser.add_argument(
        "-m",
        "--method",
        dest="method",
        required=False,
        default="exif",
        help="Method to extract the files creation date based on 'ctime', 'mtime' or 'exif' (default).",
    )
    parser.add_argument(
        "-n",
        "--nesting",
        dest="nesting",
        type=str,
        required=False,
        default="d",
        help="Structure of target directory, 'Y'ear, 'm'onth, 'd'ay (default), 'H'our, 'M'inutes.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        required=False,
        default=False,
        help="Execute quietly and suppress all output.",
    )
    parser.add_argument(
        "-s",
        "--single",
        dest="single",
        required=False,
        default=False,
        help="Whether to have a single directory of the form 'YYYY-mm[-dd[-HH[-MM]]]' rather than a nested structure.",
    )
    return parser


def find(base: str | Path = "./", ext: str = "jpg") -> list[Path]:
    """
    Find files of a given type.

    Parameters
    ----------
    base : str | Path
        Directory to search for files.
    ext : str
        File extension to search for.

    Returns
    -------
    list
        List of found files.
    """
    return list(Path(base).rglob(f"*.{ext}"))


def get_file_date(file: Path, method: str = "exif") -> float:
    """
    Extract created date from file.

    Parameters
    ----------
    file : Path
        File to extract created date from.
    method : str
        Date/time extraction method to use, currently supports exif (default), ctime and mtime.

    Returns
    -------
    float
        Returns the date as an elapsed float from origin.
    """
    file_date = _get_file_date(method)
    return file_date(file)  # type: ignore[no-any-return]


def _get_file_date(method: str = "exif") -> typing.Callable:  # type: ignore[type-arg]
    """
    Creator component which determines which date/time extraction method to use.

    Parameters
    ----------
    method : str
        Date/time extraction method to use, currently supports ctime (default), mtime.

    Returns
    -------
    function
        Returns the appropriate function for the required date/time extraction method.

    Raises
    ------
    ValueError
        Unsupported methods result in ValueError.
    """
    if method == "exif":
        return _file_date_exif
    if method == "ctime":
        return _file_date_ctime
    if method == "mtime":
        return _file_date_mtime
    raise ValueError(f"Invalid method provided : {method}")


def _file_date_ctime(file: Path) -> float:
    """
    Extract ctime from a file.

    Parameters
    ----------
    file : Path
        Path to a file.

    Returns
    -------
    float
        POSIX format ctime for the file.
    """
    try:
        return Path.stat(file).st_ctime
    except FileNotFoundError as fnfe:
        raise fnfe


def _file_date_mtime(file: Path) -> float:
    """
    Extract mtime from a file.

    Parameters
    ----------
    file : Path
        Path to a file.

    Returns
    -------
    float
        POSIX format mtime for the file.
    """
    try:
        return Path.stat(file).st_mtime
    except FileNotFoundError as fnfe:
        raise fnfe


def _file_date_exif(file: Path) -> float:
    """
    Extract file creation time from Exif data.

    Parameters
    ----------
    file : Path
        Path to a file.

    Returns
    -------
    float
        POSIX format Exif timestamp for the file.
    """
    try:
        img = Image.open(file)
        img_exif = img.getexif()
        return datetime.strptime(img_exif[306], format("%Y:%m:%d %H:%M:%S")).timestamp()
    except FileNotFoundError as fnfe:
        raise fnfe


def create_target_dir(destination: str | Path = "./", quiet: bool = True) -> None:
    """
    Create the target directory.

    Parameters
    ----------
    destination : str | Path
        Path where target directory structure is to be created.
    quiet : bool
        Report creation of target directory.

    Returns
    -------
    None
        Does not return anything, simply creates the target directory.
    """
    Path(destination).mkdir(parents=True, exist_ok=True)
    if quiet:
        logger.info(f"Created target directory : {destination}")


def construct_date_time(file_creation: float, nesting: str | None = None, single: bool = False) -> str:
    """
    Construct date and time from a file creation date.

    Parameters
    ----------
    file_creation : float
        Date and time of file creation.
    nesting : str
        Level of nesting to extract, values are 'Y'ear, 'm'onth, 'd'ay, 'H'our, 'M'inutes. Defaults to 'd'ay if not
        specified.
    single : bool
        Whether to make target directory a single rather than nested structure.

    Returns
    -------
    str
        Directory structure to create with given level of nesting.
    """
    local_file_creation = time.localtime(file_creation)
    sep = "-" if single else "/"
    if nesting == "Y":
        return time.strftime("%Y", local_file_creation)
    if nesting == "m":
        return time.strftime(f"%Y{sep}%m", local_file_creation)
    if nesting == "d":
        return time.strftime(f"%Y{sep}%m{sep}%d", local_file_creation)
    if nesting == "H":
        return time.strftime(f"%Y{sep}%m{sep}%d{sep}%H", local_file_creation)
    if nesting == "M":
        return time.strftime(f"%Y{sep}%m{sep}%d{sep}%H{sep}%M", local_file_creation)
    return time.strftime(f"%Y{sep}%m{sep}%d", local_file_creation)


def move_file(source: Path, destination: Path, quiet: bool = True) -> Path:
    """
    Move a file.

    Parameters
    ----------
    source : Path
        Path to the source file.
    destination : Path
        Destination directory.
    quiet : bool
        Suppress logging output.

    Returns
    -------
    Path
        Returns the Path the file is moved to.
    """
    source = Path(source)
    destination = Path(destination) / source.name
    try:
        destination = shutil.move(source, destination)
        if quiet:
            logger.info(f"Moved : {source} -> {destination}")
        return destination
    except FileNotFoundError as fnfe:
        raise fnfe


def main(args: arg.ArgumentParser | None = None) -> None:
    """
    Find and move files.

    Parameters
    ----------
    args : arg.ArgumentParser
        Arguments to run the function with.
    """
    parser = create_parser()
    args = parser.parse_args() if args is None else parser.parse_args(args)  # type: ignore[call-overload, assignment]
    arguments = vars(args)
    # Find files
    files_to_move = find(base=Path(arguments["base"]), ext=arguments["ext"])
    if arguments["quiet"]:
        f = Figlet(font="slant")
        print(f.renderText("mvdate"))
        logger.info(f"Search directory                           : {arguments['base']}")
        logger.info(f"Searching for files with extension         : {arguments['ext']}")
        logger.info(f"Files found                                : {len(files_to_move)}")
    # Extract all file dates
    all_file_dates = [get_file_date(x, method=arguments["method"]) for x in list(files_to_move)]
    # Extract target directories, making a unique set
    all_target_dirs = [
        construct_date_time(x, nesting=arguments["nesting"], single=arguments["single"]) for x in all_file_dates
    ]
    target_dirs = set(all_target_dirs)
    # Create target directories
    for x in target_dirs:
        create_target_dir(x, arguments["quiet"])  # pylint: disable=expression-not-assigned
    # Move files
    for file_to_move, all_target_dir in tqdm(
        zip(list(files_to_move), all_target_dirs, strict=True), desc=f"Moving {len(files_to_move)} files."
    ):
        move_file(Path(file_to_move), Path(all_target_dir), arguments["quiet"])
