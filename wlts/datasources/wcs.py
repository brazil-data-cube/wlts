#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS WCS DataSource."""
from functools import lru_cache

from owslib.util import Authentication
from owslib.wcs import WebCoverageService
from rasterio.io import MemoryFile
from shapely.geometry import Point, mapping

from wlts.datasources.datasource import DataSource
from wlts.utils import get_date_from_str


class WCS:
    """This class implements the WCS client.."""

    def __init__(self, host, **kwargs):
        """Create a WCS client attached to the given host address (an URL).

        Args:
            host (str): the server URL.
            **kwargs: The keyword arguments with credentials to access OGC WCS.
        """
        invalid_parameters = set(kwargs) - {"username", "password"}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        if 'username' in kwargs:
                auth = Authentication(username=kwargs['username'], password=kwargs['password'])
                self.wcs_owslib = WebCoverageService(host, version='1.0.0', auth=auth)
        else:
            self.wcs_owslib = WebCoverageService(host, version='1.0.0')

    def _get(self, name, bbox, width, height, time, x, y):
        """Return the image value for a location.

        Args:
            name (str): The image(coverage) name to retrieve from service.
            bbox (str): The extent of the image(coverage) to retrieve.
            x (int/float): A longitude value according to EPSG:4326.
            y (int/float): A latitude value according to EPSG:4326.
        """
        output = self.wcs_owslib.getCoverage(identifier=name, format='GeoTIFF',
                                             bbox=bbox,
                                             crs='EPSG:4326',
                                             time=[time],
                                             width=width, height=height)

        data = output.read()

        try:
            memfile = MemoryFile(data)
            dataset = memfile.open()

            values = list(dataset.sample([(x, y)]))

            memfile = None
            dataset = None
            data = None

            return values[0]
        except:
            return None

    @lru_cache()
    def get_image(self, image, min_x, max_x, min_y, max_y, width, height, time, x, y):
        """Returns the image value."""
        bbox = (min_x, min_y, max_x, max_y)

        image_infos = self._get(image, bbox, width, height, time, x, y)

        return image_infos

    def list_image(self):
        """Returns the list of all available image in service."""
        return self.wcs_owslib.contents.keys()


class WCSDataSource(DataSource):
    """This class implemente a WCSDataSource."""

    def __init__(self, id, ds_info):
        """Create a WCSDataSource.

        Args:
            id (str): the datasource identifier.
            ds_info (dict): A datasource information as a dictionary.
        """
        super().__init__(id)

        if 'username' in ds_info and 'password' in ds_info:
            self._wcs = WCS(ds_info['host'], username=ds_info["username"], password=ds_info["password"])
        else:
            self._wcs = WCS(ds_info['host'])

        self.workspace = ds_info['workspace']

    def get_type(self):
        """Return the datasource type."""
        return "WCS"

    def check_image_exist(self, ft_name):
        """Utility to check image existence in wcs.

        Args:
            ft_name (str): The image name.
        """
        images = self._wcs.list_image()

        if ft_name not in images:
            raise ValueError(f'Image "{ft_name}" not found in host {self._wcs.url}')
        
    def organize_trajectory(self, result, time, classification_class, geom, geom_flag, temporal):
        """Organize trajectory."""
        # Get temporal information
        obs_info = get_date_from_str(time)
        obs_info = obs_info.strftime(temporal["string_format"])
    
        # Get Class
        if classification_class.get_type() == "Self":
            class_info = result['raster_value']
        else:
            ds_class = classification_class.get_class_ds()

            class_info = ds_class.get_classe(result,
                                             classification_class.get_class_property_value(),
                                             classification_class.get_class_property_name(),
                                             classification_class.get_property_name(),
                                             class_system=classification_class.get_classification_system_name())

        trj = dict()
        trj["class"] = class_info
        trj["date"] = str(obs_info)

        if geom_flag:
            trj["geom"] = mapping(geom)
        
        return trj

    def get_trajectory(self, **kwargs):
        """Return a trajectory instance for wcs datasource.

        Args:
            **kwargs: The keyword arguments.
        """
        invalid_parameters = set(kwargs) - {"image", "temporal",
                                            "x", "y", "srid",
                                            "grid", "start_date", "end_date", "time", "classification_class",
                                            "geometry_flag"}
        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        ts = get_date_from_str(kwargs['time'])

        if kwargs['start_date']:
            start_date = get_date_from_str(kwargs['start_date'])
            if ts < start_date:
                return None
        if kwargs['end_date']:
            end_date = get_date_from_str(kwargs['end_date'])
            if ts > end_date:
                return None

        image_name = self.workspace + ":" + kwargs['image']

        min_x, min_y, max_x, max_y = Point(kwargs['x'], kwargs['y']).buffer(0.002).bounds

        image_infos = self._wcs.get_image(image_name, min_x, max_x, min_y, max_y,
                                          (kwargs['grid'])['column'],
                                          (kwargs['grid'])['row'],
                                          kwargs['time'], kwargs['x'], kwargs['y'])

        if image_infos is not None:
            trj = self.organize_trajectory(result=image_infos, time=kwargs['time'],
                                           classification_class=kwargs['classification_class'],
                                           geom=Point(kwargs['x'], kwargs['y']),
                                           geom_flag=kwargs['geometry_flag'],
                                           temporal=kwargs['temporal']
                                           )

            return trj

        return image_infos
