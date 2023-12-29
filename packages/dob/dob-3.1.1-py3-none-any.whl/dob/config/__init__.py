# This file exists within 'dob':
#
#   https://github.com/tallybark/dob
#
# Copyright © 2018-2020 Landon Bouma,  2015-2016 Eric Goller.  All rights reserved.
#
# 'dob' is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License  as  published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any   later    version.
#
# 'dob' is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY  or  FITNESS FOR A PARTICULAR
# PURPOSE.  See  the  GNU General Public License  for  more details.
#
# You can find the GNU General Public License reprinted in the file titled 'LICENSE',
# or visit <http://www.gnu.org/licenses/>.

"""``dob`` functions that deal with application-specific config."""

# Set config file basename, e.g., 'dob.conf'.
from . import conf_filename  # noqa: F401

# Set envvar_prefix, e.g., 'set | grep '^DOB_'.
from . import envvar_prefix  # noqa: F401

# Wire AppDirs, e.g., ~/.config/dob, ~/.cache/dob, etc.
from . import init_app_dirs  # noqa: F401
