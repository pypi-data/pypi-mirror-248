# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from functools import cache

from lsst.daf.butler import Butler
from lsst.daf.butler.direct_butler import DirectButler

from ._config import get_config_from_env
from ._factory import Factory


@cache
def _make_global_butler() -> DirectButler:
    config = get_config_from_env()
    butler = Butler.from_config(config.config_uri)
    if not isinstance(butler, DirectButler):
        raise TypeError("Server can only use a DirectButler")
    return butler


def factory_dependency() -> Factory:
    """Return factory dependency for injection into FastAPI."""
    return Factory(butler=_make_global_butler())
