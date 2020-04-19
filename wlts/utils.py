#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils for Web Land Trajectory Service."""

from pkg_resources import resource_string as load


def load_exemple_data(file):
    """Load data."""
    sql_dir = "example/{}".format(file)

    sql = load(__name__, sql_dir).decode()

    return sql