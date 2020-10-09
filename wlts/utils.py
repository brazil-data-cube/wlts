#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils for Web Land Trajectory Service."""
from datetime import datetime

from osgeo import osr
from pkg_resources import resource_string as load


def load_example_data(file):
    """Load data."""
    sql_dir = "example/{}".format(file)

    sql = load(__name__, sql_dir).decode()

    return sql


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


def transform_latlong_to_rowcol(data_set, lat, long):
    """Transform the pixel location of a geospatial coordinate."""
    srs = osr.SpatialReference()
    srs.ImportFromWkt(data_set.GetProjection())

    srs_lat_long = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs_lat_long, srs)
    x, y, _ = ct.TransformPoint(long, lat)

    transform = data_set.GetGeoTransform()

    x = int((x - transform[0]) / transform[1])
    y = int((transform[3] - y) / -transform[5])

    return x, y
