#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS WFS DataSource."""
import requests
from xml.dom import minidom
from json import loads as json_loads
from werkzeug.exceptions import NotFound
from shapely.geometry import Point

from wlts.datasources.datasource import DataSource
from wlts.utils import get_date_from_str

class WFS():
    """WFSOperations.

    :param host: Host
    :type host: string.

    """

    def __init__(self, host, **kwargs):
        """Create a WFS client attached to the given host address (an URL)."""
        invalid_parameters = set(kwargs) - {"auth"}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self.host = host
        self.base_path = "wfs?service=WFS&version=1.0.0"

        self._auth = None

        if 'auth' in kwargs:
            if kwargs['auth'] is not None:
                if not type(kwargs['auth']) is tuple:
                    raise AttributeError('auth must be a tuple ("user", "pass")')
                if len(kwargs['auth']) != 2:
                    raise AttributeError('auth must be a tuple with 2 values ("user", "pass")')
                self._auth = kwargs['auth']

    def _get(self, uri):
        """Get WFS."""
        response = requests.get(uri, auth=self._auth)

        if (response.status_code) != 200:
            raise Exception("Request Fail: {} ".format(response.status_code))

        return response.content.decode('utf-8')

    def _list_features(self):
        """List Features."""
        url = "{}/{}&request=GetCapabilities&outputFormat=application/json".format(self.host, self.base_path)

        doc = self._get(url)

        xmldoc = minidom.parseString(doc)
        itemlist = xmldoc.getElementsByTagName('FeatureType')

        features = dict()
        features[u'features'] = []

        for s in itemlist:
            features[u'features'].append(s.childNodes[0].firstChild.nodeValue)

        return features

    def check_feature(self, ft_name):
        """Utility to check feature existence in wfs."""
        features = self._list_features()

        if ft_name not in features['features']:
            raise NotFound('Feature "{}" not found'.format(ft_name))

    def get_feature(self, **kwargs):
        """Retrieve the feature collection given feature."""
        invalid_parameters = set(kwargs) - {'typeName', 'srid', 'propertyName', 'filter'}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        #TODO verificar a feature
        # self.check_feature(kwargs['typeName'])

        url = "{}/{}&request=GetFeature&typeName={}".format(self.host, self.base_path, kwargs['typeName'])

        if 'propertyName' in kwargs:
            url += "&propertyName={}".format(kwargs['propertyName'])

        url += "&outputformat=json"

        url += "&CRS=EPSG:{}".format(kwargs['srid'])

        if 'filter' in kwargs:
            if type(kwargs['filter']) is not str:
                raise AttributeError('filter must be a string')
            url += kwargs['filter']

        doc = self._get(url)

        js = json_loads(doc)

        if not js["features"]:
            return None
        else:
            return js["features"][0]["properties"]

    def get_class(self, featureID, **kwargs):
        """Get classes of given feature."""
        invalid_parameters = set(kwargs) - {'value', 'class_property_name', 'typeName', 'tagName'}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))


        #TODO verificar os parametros
        #TODO verficar se a feature de class existe

        url = "{}/{}&request=GetFeature&typeName={}&cql_filter={}={}".format(self.host,"wfs?service=WFS&version=1.0.0",
                                                                             kwargs['typeName'], kwargs['value'],
                                                                             featureID)
        doc = self._get(url)

        xmldoc = minidom.parseString(doc)

        itemlist = xmldoc.getElementsByTagName(kwargs['tagName'])

        return itemlist[0].firstChild.nodeValue

class WFSDataSource(DataSource):
    """WFS DataSource Class."""

    def __init__(self, id, ds_info):
        """Init Method of WFSDataSource."""
        super().__init__(id)

        if 'user' in  ds_info and 'password' in ds_info:
            self._wfs = WFS(ds_info['host'], auth=(ds_info["user"], ds_info["password"]))
        else:
            self._wfs = WFS(ds_info['host'])

        self.workspace = ds_info['workspace']

    def get_type(self):
        """WFS DataSource Type."""
        return "WFS"

    def get_classe(self, featureID, value, class_property_name, ft_name):
        """Get Class."""
        typeName = self.workspace + ":" + ft_name

        tagName = self.workspace + ":" + class_property_name

        return  self._wfs.get_class(featureID=featureID, value=value,
                            typeName=typeName, tagName=tagName)

    def get_trajectory(self, **kwargs):
        """Get Trajectory."""
        invalid_parameters = set(kwargs) - {"feature_name", "temporal",
                                                    "x", "y", "obs", "geom_property",
                                                    "classification_class", "start_date", "end_date"}
        if invalid_parameters:
                    raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        typeName = self.workspace + ":" + kwargs['feature_name']

        geom = Point(kwargs['x'], kwargs['y'])

        cql_filter = "&CQL_FILTER=INTERSECTS({}, {})".format((kwargs['geom_property'])['property_name'] , geom.wkt)

        if (kwargs['temporal'])["type"] == "STRING":

            temporal_observation = get_date_from_str((kwargs['obs'])["temporal_property"])

            if kwargs['start_date']:
                start_date = get_date_from_str(kwargs['start_date'])
                if (start_date > temporal_observation):
                    return
            if kwargs['end_date']:
                end_date = get_date_from_str(kwargs['end_date'])
                if (temporal_observation > end_date):
                    return
        else:
            if kwargs['start_date']:
                start_date = get_date_from_str(kwargs['start_date'])
                cql_filter += " AND {} >= {}".format((kwargs['obs'])["temporal_property"],
                                                           start_date.strftime((kwargs['temporal'])["string_format"]))

            if kwargs['end_date'] :
                end_date = get_date_from_str(kwargs['end_date'])
                cql_filter += " AND {} <= {}".format((kwargs['obs'])["temporal_property"],
                                                         end_date.strftime((kwargs['temporal'])["string_format"]))

        args = {
            "typeName": typeName,
            "filter": cql_filter,
            "srid": (kwargs['geom_property'])['srid']
        }

        retval = self._wfs.get_feature(**args)

        return retval
