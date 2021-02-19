#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils for Web Land Trajectory Service."""
from datetime import datetime


def get_date_from_str(date, date_ref=None):
    """Utility to build date from str."""
    date = date.replace('/', '-')

    try:
        date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        try:
            date = datetime.strptime(date, '%Y-%m')
        except ValueError:
            date = datetime.strptime(date, '%Y')

    if date_ref:
        date = date.replace(day=31, month=12)

    return date
