"""A package for moving files based on various dates."""
from importlib.metadata import version

# Copyright 2020 Neil Shephard
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

release = version("mvdate")
__version__ = ".".join(release.split("."[:2]))
