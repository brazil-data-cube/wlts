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
