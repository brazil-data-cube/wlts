#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS WFS DataSource."""
from functools import lru_cache
from json import loads as json_loads
from xml.dom import minidom

import requests
from shapely.geometry import MultiPolygon, Point, Polygon, mapping
from werkzeug.exceptions import NotFound

from wlts.datasources.datasource import DataSource
from wlts.utils.utilities import get_date_from_str, transform_crs


class WFS:
    """This class implements the WCS client."""

    def __init__(self, host, **kwargs):
        """Create a WFS client attached to the given host address (an URL).

        Args:
            host (str): the server URL.
            **kwargs: The keyword arguments with credentials to access WFS.
        """
        invalid_parameters = set(kwargs) - {"auth"}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self._host = host
        self._base_path = "wfs?service=WFS&version=1.0.0"

        self._auth = None

        if 'auth' in kwargs:
            if kwargs['auth'] is not None:
                if not type(kwargs['auth']) is tuple:
                    raise AttributeError('auth must be a tuple ("user", "pass")')
                if len(kwargs['auth']) != 2:
                    raise AttributeError('auth must be a tuple with 2 values ("user", "pass")')
                self._auth = kwargs['auth']

    @property
    def host_information(self) -> str:
        """Returns the host."""
        return self._host

    def _get(self, uri):
        """Query the WFS service using HTTP GET verb.

        Args:
            uri (str): URL for the WCS server.
        """
        response = requests.get(uri, auth=self._auth)

        if response.status_code != 200:
            raise Exception("Request Fail: {} ".format(response.status_code))

        return response.content.decode('utf-8')

    def _list_features(self):
        """Returns the list of all available feature in service."""
        url = "{}/{}&request=GetCapabilities&outputFormat=application/json".format(self._host, self._base_path)

        doc = self._get(url)

        xmldoc = minidom.parseString(doc)
        itemlist = xmldoc.getElementsByTagName('FeatureType')

        features = dict()
        features[u'features'] = []

        for s in itemlist:
            features[u'features'].append(s.childNodes[0].firstChild.nodeValue)

        return features

    def check_feature(self, ft_name):
        """Utility to check feature existence in wfs.

        Args:
            ft_name (str): The feature name to check.
        """
        features = self._list_features()

        if ft_name not in features['features']:
            raise NotFound('Feature "{}" not found'.format(ft_name))

    def mount_url(self, type_name, **kwargs):
        """Mount the url for get a feature from server based on GetFeature request.

        Args:
            type_name (str): Name of the feature type.
            **kwargs: The keyword arguments:
                srid (int): EPSG code
                propertyName (str): Feature property names
                filter (str): Filter to use in request.
                outputformat (str): Requested response format of the request.

        """
        invalid_parameters = set(kwargs) - {'srid', 'propertyName', 'filter', 'outputformat'}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        url = "{}/{}&request=GetFeature&typeName={}".format(self._host, self._base_path, type_name)

        if 'propertyName' in kwargs:
            url += "&propertyName={}".format(kwargs['propertyName'])

        if 'outputformat' in kwargs:
            url += kwargs['outputformat']

        if 'srid' in kwargs:
            url += "&CRS=EPSG:{}".format(kwargs['srid'])

        if 'filter' in kwargs:
            if type(kwargs['filter']) is not str:
                raise AttributeError('filter must be a string')
            url += kwargs['filter']

        return url

    def get_feature(self, type_name, srid, filter):
        """Retrieve the feature collection given feature."""
        args = {"srid": srid, "filter": filter, "outputformat": "&outputformat=json"}

        url = self.mount_url(type_name, **args)

        doc = self._get(url)

        js = json_loads(doc)

        if not js["features"]:
            return None
        else:
            return js["features"]

    @lru_cache()
    def get_class(self, type_name, tag_name, filter):
        """Return a class of given feature."""
        args = {"filter": "&cql_filter={}".format(filter)}

        url = self.mount_url(type_name, **args)

        doc = self._get(url)

        xmldoc = minidom.parseString(doc)

        itemlist = xmldoc.getElementsByTagName(tag_name)

        return itemlist[0].firstChild.nodeValue


class WFSDataSource(DataSource):
    """This class implements a WFSDataSource."""

    def __init__(self, id, ds_info):
        """Create a WFSDataSource.

        Args:
            id (str): the datasource identifier.
            ds_info (dict): A datasource information as a dictionary.
        """
        super().__init__(id)

        if 'user' in ds_info and 'password' in ds_info:
            self._wfs = WFS(ds_info['host'], auth=(ds_info["user"], ds_info["password"]))
        else:
            self._wfs = WFS(ds_info['host'])

        if 'external_host' in ds_info:
            self._external_host = ds_info['external_host']
        else:
            self._external_host = ds_info['host']


    def get_type(self):
        """Return the datasource type."""
        return "WFS"
    
    @property
    def host_information(self) -> str:
        """Returns the host."""
        return self._external_host

    def get_classe(self, feature_id, value, class_property_name, ft_name, workspace, **kwargs):
        """Return a class of feature based on his classification system."""
        type_name = workspace + ":" + ft_name
        tag_name = workspace + ":" + class_property_name

        if 'class_system' in kwargs:
            filter = "{}={} AND class_system_name=\'{}\'".format(value, feature_id, kwargs['class_system'])
        else:
            filter = "{}={}".format(value, feature_id)

        return self._wfs.get_class(type_name=type_name, tag_name=tag_name, filter=filter)

    def organize_trajectory(self, result, obs, geom_flag, geom_property, classification_class, temporal):
        """Organize trajectory."""
        # Get temporal information
        if temporal["type"] == "STRING":
            obs_info = get_date_from_str(obs["temporal_property"])
            obs_info = obs_info.strftime(temporal["string_format"])
            obs_info = obs_info.replace('Z', '')

        elif temporal["type"] == "DATE":
            obs_info = result['properties'][obs["temporal_property"]]
            if isinstance(obs_info, str):
                obs_info = obs_info.replace('Z', '')
        # Get Class information
        if classification_class.type == "Literal":
            class_info = obs["class_property_name"]
    
        elif classification_class.type == "Self":
            class_info = result['properties'][obs["class_property"]]
        else:
            feature_id = result['properties'][obs["class_property"]]

            ds_class = classification_class.get_class_ds()

            if classification_class.classification_system_name is None:
                class_info = ds_class.get_classe(feature_id=feature_id,
                                                 value=classification_class.class_property_value,
                                                 class_property_name=classification_class.class_property_name,
                                                 ft_name=classification_class.property_name)
            else:
                class_info = ds_class.get_classe(feature_id=feature_id,
                                                 value=classification_class.class_property_value,
                                                 class_property_name=classification_class.class_property_name,
                                                 ft_name=classification_class.property_name,
                                                 workspace=classification_class.workspace,
                                                 class_system=classification_class.classification_system_name)
        trj = dict()
        trj["class"] = class_info
        trj["date"] = str(obs_info)

        if geom_flag:
            if result['geometry']['type'] == 'Point':
                geom = Point(result['geometry']['coordinates'][0], result['geometry']['coordinates'][1])
            elif result['geometry']['type'] == 'MultiPolygon':
                polygons = []
                for polygon in result['geometry']['coordinates']:
                    polygons += [Polygon(lr) for lr in polygon]
                geom = MultiPolygon(polygons)
            elif result['geometry']['type'] == 'Polygon':
                geom = Polygon(result['geometry']['coordinates'][0])
            else:
                raise Exception('Unsupported geometry type.')
        
            crs_orig = f'EPSG:{geom_property}'
            geom_tmp = transform_crs(crs_orig, 'EPSG:4326', geom)

            trj["geom"] = mapping(geom_tmp)

        return trj

    def get_trajectory(self, **kwargs):
        """Return a trajectory observation of this datasource."""
        invalid_parameters = set(kwargs) - {"temporal", "x", "y", "obs", "geom_property",
                                            "classification_class", "start_date", "end_date", "geometry_flag"}
        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        type_name =  (kwargs['obs'])['workspace'] + ":" + (kwargs['obs'])['feature_name']

        geom = Point(kwargs['x'], kwargs['y'])

        cql_filter = "&CQL_FILTER=INTERSECTS({}, {})".format((kwargs['geom_property'])['property_name'], geom.wkt)

        if (kwargs['temporal'])["type"] == "STRING":
            temporal_observation = get_date_from_str((kwargs['obs'])["temporal_property"]).strftime(
                (kwargs['temporal'])["string_format"])
            if kwargs['start_date']:
                start_date = get_date_from_str(kwargs['start_date']).strftime((kwargs['temporal'])["string_format"])
                if start_date > temporal_observation:
                    return
            if kwargs['end_date']:
                end_date = get_date_from_str(kwargs['end_date']).strftime((kwargs['temporal'])["string_format"])
                if temporal_observation > end_date:
                    return
        else:
            if kwargs['start_date']:
                start_date = get_date_from_str(kwargs['start_date'])
                cql_filter += " AND {} >= {}".format((kwargs['obs'])["temporal_property"],
                                                     start_date.strftime((kwargs['temporal'])["string_format"]))

            if kwargs['end_date']:
                end_date = get_date_from_str(kwargs['end_date'])
                cql_filter += " AND {} <= {}".format((kwargs['obs'])["temporal_property"],
                                                     end_date.strftime((kwargs['temporal'])["string_format"]))

        retval = self._wfs.get_feature(type_name, (kwargs['geom_property'])['srid'], cql_filter)

        trj = list()

        if retval is not None:
            for i in retval:
                trj.append(self.organize_trajectory(result=i, obs=kwargs['obs'],
                                                    geom_flag=kwargs['geometry_flag'],
                                                    geom_property=(kwargs['geom_property'])['srid'],
                                                    classification_class=kwargs['classification_class'],
                                                    temporal=kwargs['temporal']))

            return trj

        return retval
