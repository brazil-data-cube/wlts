#
# This file is part of WLTS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Unit-test for WLTS' controller."""
import pytest
import datetime

from wlts.utils.utilities import get_date_from_str, transform_crs


def test_get_date_from_str():
    test_date = datetime.datetime(2016, 1, 1, 0, 0)
    date = get_date_from_str("2016")

    assert test_date == test_date
    assert isinstance(date, datetime.datetime)
