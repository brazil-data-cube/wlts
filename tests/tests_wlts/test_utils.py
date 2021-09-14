#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
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
