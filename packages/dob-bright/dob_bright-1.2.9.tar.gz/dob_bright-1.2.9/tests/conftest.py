# This file exists within 'dob-bright':
#
#   https://github.com/tallybark/dob-bright
#
# Copyright © 2020 Landon Bouma. All rights reserved.
#
# This program is free software:  you can redistribute it  and/or  modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3  of the License,  or  (at your option)  any later version  (GPLv3+).
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or  FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU  General  Public  License  for  more  details.
#
# If you lost the GNU General Public License that ships with this software
# repository (read the 'LICENSE' file), see <http://www.gnu.org/licenses/>.

""""""

# For the fixture to work, either import what you need, or glob it all.
# - Globbing is easier and more akin to how conftest.py normally magically works.
# - Skip the linter's two gripes:
#    noqa: F401 'foo.bar' imported but unused
#    noqa: F403 'from foo.bar import *' used; unable to detect undefined names
from dob_bright.tests.conftest import *  # noqa: F401, F403

pytest_plugins = (
    # Import tmp_appdirs fixture.
    "easy_as_pypi_appdirs.tests.appdirs_mock",
    # Set KeyChainedValue._envvar_prefix.
    "tests.config.envvar_prefix",
    # Call app_dirs.register_application.
    "tests.config.init_app_dirs",
    "nark.tests.backends.sqlalchemy.conftest",
    # Make sure fixtures required by fixtures available, e.g., 'base_config'.
    "nark.tests.conftest",
)
