#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils for Web Land Trajectory Service."""
from datetime import datetime

import pyproj
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform


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


def transform_crs(crs_src: str, crs_dest: str, geom: BaseGeometry) -> BaseGeometry:
    """Reproject geometry.
    
    Args:
        crs_src (str): Actual geometry CRS.
        crs_dest (str): Destiny geometry CRS.
        geom (shapely.geometry.base.BaseGeometry): Shapely Geometry.
    Returns:
        shapely.geometry.base.BaseGeometry: Shapely Geometry reprojected.
    """
    crs_src = pyproj.CRS(crs_src)
    crs_dest = pyproj.CRS(crs_dest)
    
    transform_fnc = pyproj.Transformer.from_crs(crs_src, crs_dest).transform
    
    return transform(transform_fnc, geom)
