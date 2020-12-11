#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS WCS DataSource."""
import base64
import urllib.request
from functools import lru_cache
from uuid import uuid4
from xml.dom import minidom

import requests
from osgeo import gdal
from shapely.geometry import Point
from werkzeug.exceptions import NotFound

from wlts.datasources.datasource import DataSource
from wlts.utils import get_date_from_str, transform_latlong_to_rowcol


class WCS:
    """This class implements the WCS client.."""

    def __init__(self, host, **kwargs):
        """Create a WCS client attached to the given host address (an URL).

        Args:
            host (str): the server URL.
            **kwargs: The keyword arguments with credentials to access WFS.
        """
        invalid_parameters = set(kwargs) - {"auth"}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self.host = host
        self.base_path = "wcs?service=WCS&version=1.0.0"

        self._auth = None

        if 'auth' in kwargs:
            if kwargs['auth'] is not None:
                if not type(kwargs['auth']) is tuple:
                    raise AttributeError('auth must be a tuple ("user", "pass")')
                if len(kwargs['auth']) != 2:
                    raise AttributeError('auth must be a tuple with 2 values ("user", "pass")')
                self._auth = kwargs['auth']

    def _get_image(self, uri):
        """Query the WCS service using HTTP GET verb and return the image result.

        Args:
            uri (str): URL for the WCS server.
        """
        if self._auth:
            request = urllib.request.Request(uri)

            credentials = ('%s:%s' % (self._auth[0], self._auth[1])).replace('\n', '')
            encoded_credentials = base64.b64encode(credentials.encode('ascii'))

            request.add_header('Accept-Encoding', "gzip")
            request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

        else:
            request = urllib.request.Request(uri, headers={"Accept-Encoding": "gzip"})

        try:
            response = urllib.request.urlopen(request, timeout=30)
            if response.info().get('Content-Encoding') == 'gzip':
                return None
            else:
                return response
        except urllib.request.URLError:
            return None

    def _get(self, uri):
        """Query the WCS service using HTTP GET verb.

        Args:
            uri (str): URL for the WCS server.
        """
        response = requests.get(uri, auth=self._auth)

        if response.status_code != 200:
            raise Exception("Request Fail: {} ".format(response.status_code))

        return response.content.decode('utf-8')

    def list_image(self):
        """Returns the list of all available image in service."""
        url = "{}/{}&request=GetCapabilities&outputFormat=application/json".format(self.host, self.base_path)

        doc = self._get(url)

        xmldoc = minidom.parseString(doc)

        itemlist = xmldoc.getElementsByTagName('wcs:ContentMetadata')

        avaliables = []

        for s in itemlist[0].childNodes:
            avaliables.append(s.childNodes[0].firstChild.nodeValue)

        return avaliables

    def check_image(self, ft_name):
        """Utility to check image existence in wcs.

        Args:
            ft_name (str): The image name.
        """
        images = self.list_image()

        if ft_name not in images:
            raise NotFound('Image "{}" not found'.format(ft_name))

    def open_image(self, url, long, lat):
        """Return the image value for a location.

        Args:
            url (str): URL for the WCS server.
            long (int/float): A longitude value according to EPSG:4326.
            lat (int/float): A latitude value according to EPSG:4326.
        """
        image_data = self._get_image(url)

        if not image_data:
            return None

        mmap_name = "/vsimem/" + uuid4().hex

        gdal.FileFromMemBuffer(mmap_name, image_data.read())
        gdal_dataset = gdal.Open(mmap_name)

        if gdal_dataset is not None:
            x, y = transform_latlong_to_rowcol(gdal_dataset, lat, long)

            intval = gdal_dataset.GetRasterBand(1).ReadAsArray(x, y, 1, 1).astype("int")

            gdal_dataset = None
            # Free memory associated with the in-memory file
            gdal.Unlink(mmap_name)

            if intval is not None:
                return intval[0][0]
            else:
                return intval

        else:
            return None

    @lru_cache()
    def get_image(self, image, srid, min_x, max_x, min_y, max_y, column, row, time, x, y):
        """Mount the url for get a image(coverage) from server based on GetCoverage request.

        Args:
            image (str): The image(coverage) name to retrieve from service.
            srid (int): The CRS of the image(coverage).
            min_x (int/float): The min x the extent of the image(coverage)
            max_x (int/float): The max x the extent of the image(coverage)
            min_y (int/float): The min y the extent of the image(coverage)
            max_y (int/float): The max y the extent of the image(coverage)
            column (int): Grid resolution.
            row (int): Grid resolution.
            time (str): Time dimension.
            x (int/float): The location x to retrieve.
            x (int/float): The location y to retrieve.
        """
        url = "{}/{}&request=GetCoverage&COVERAGE={}&".format(self.host, self.base_path, image)

        url += "CRS=EPSG:4326&RESPONSE_CRS=EPSG:{}&".format(srid)

        url += "BBOX={},{},{},{}".format(min_x, max_x, min_y, max_y)

        url += "&FORMAT=GeoTIFF&WIDTH={}&HEIGHT={}&time={}".format(column, row, time)

        image_value = self.open_image(url, x, y)

        return image_value


class WCSDataSource(DataSource):
    """This class implemente a WCSDataSource."""

    def __init__(self, id, ds_info):
        """Create a WCSDataSource.

        Args:
            id (str): the datasource identifier.
            ds_info (dict): A datasource information as a dictionary.
        """
        super().__init__(id)

        if 'user' in ds_info and 'password' in ds_info:
            self._wcs = WCS(ds_info['host'], auth=(ds_info["user"], ds_info["password"]))
        else:
            self._wcs = WCS(ds_info['host'])

        self.workspace = ds_info['workspace']

    def get_type(self):
        """Return the datasource type."""
        return "WCS"

    def get_trajectory(self, **kwargs):
        """Return a trajectory instance for wcs datasource.

        Args:
            **kwargs: The keyword arguments.
        """
        invalid_parameters = set(kwargs) - {"image", "temporal",
                                            "x", "y", "srid",
                                            "grid", "start_date", "end_date", "time"}
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

        image_value = self._wcs.get_image(image_name, kwargs['srid'],
                                      min_x, min_y, max_x, max_y,
                                      (kwargs['grid'])['column'], (kwargs['grid'])['row'],
                                      kwargs['time'], kwargs['x'], kwargs['y'])

        return image_value
