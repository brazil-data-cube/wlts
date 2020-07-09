#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Class."""
from abc import ABCMeta, abstractmethod

from wlts.datasources.ds_manager import datasource_manager
from wlts.collections.class_system import ClassificationSystemClass as Class


class Collection(metaclass=ABCMeta):
    """Abstract Collection Class."""

    def __init__(self,  name, authority_name, description, detail, datasource_id, dataset_type,
                 classification_class, temporal, scala, spatial_extent, period):
        """Create Collection."""
        print("Collection INIT")
        self.name = name
        self.authority_name = authority_name
        self.description = description
        self.detail = detail
        self.dataset_type = dataset_type
        self.temporal = temporal
        self.scala = scala
        self.spatial_extent = spatial_extent
        self.period = period
        self.classification_class = self.init_classification_system(classification_class)

        print("Init datasource")
        self.datasource = datasource_manager.get_datasource(datasource_id)
        print(self.datasource.get_id)

        # invalid_parameters = set(kwargs) - {"name", "authority_name", "description",
        #                                     "detail", "datasource_id", "dataset_type",
        #                                     "classification_class", "temporal", "scala",
        #                                     "spatial_extent", "period"}
        # if invalid_parameters:
        #     raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))
        #
        # if not type(kwargs['name']) is str:
        #     raise AttributeError('name must be str')

        # self.name = kwargs['name']
        #
        # if not type(kwargs['authority_name']) is str:
        #     raise AttributeError('authority name must be str')
        #
        # self.authority_name = kwargs['authority_name']
        #
        # if not type(kwargs['description']) is str:
        #     raise AttributeError('description must be str')
        #
        # self.description = kwargs['description']
        #
        # if not type(kwargs['detail']) is str:
        #     raise AttributeError('detail must be str')
        #
        # self.detail = kwargs['detail']
        #
        # if not type(kwargs['dataset_type']) is str:
        #     raise AttributeError('dataset_type be str')
        #
        # if (kwargs['dataset_type'] is not "Feature") or ((kwargs['dataset_type'] is not "Image")):
        #     raise AttributeError('dataset_type be Feature or Image')
        #
        # self.dataset_type = kwargs['dataset_type']
        #
        # #Todo verificar o tipo
        # self.scala = kwargs['scala']
        # self.temporal = kwargs['temporal']
        # self.spatial_extent = kwargs['spatial_extent']
        # self.period = kwargs['period']
        # self.classification_class = self.init_classification_system(kwargs['classification_class'])
        # self.datasource = datasource_manager.get_datasource(kwargs['datasource_id'])


    def init_classification_system(self, classification_class):
        """Creates Class."""
        args = dict()

        args['datasource_id'] = None

        if classification_class["type"] == 'Self':
            args['type'] = classification_class["type"]
            args['name'] = None
            args['class_name'] = None
            args['value'] = None

        else:

            args['type'] = classification_class["type"]
            args['name'] = classification_class["property_name"]
            args['class_name'] = classification_class["class_property_name"]
            args['value'] = classification_class["property_value"]


        if 'datasource_id' in classification_class:
            args['datasource_id'] = classification_class["datasource_id"]

        return Class(**args)

    def get_name(self):
        """Get Collection Name."""
        return self.name

    def get_datasource_id(self):
        """Get Collection id."""
        return self.datasource.get_id()

    def get_datasource(self):
        """Get Collection DataSource."""
        return self.datasource

    def get_resolution_unit(self):
        """Get Collection Time resolution unit."""
        return self.temporal["resolution"]["unit"]

    def get_resolution_value(self):
        """Get Collection Time resolution value."""
        return self.temporal["resolution"]["value"]

    def get_spatial_extent(self):
        """Get Collection Spatial_extent."""
        return self.spatial_extent

    def get_start_date(self):
        """Get Collection start_date."""
        return self.period["start_date"]

    def get_end_date(self):
        """Get Collection end_date."""
        return self.period["end_date"]

    @abstractmethod
    def trajectory(self, tj_attr, x, y, start_date, end_date):
        """Get Trajectory Type Abstract Method."""
        pass

    @abstractmethod
    def collection_type(self):
        """Get Collections Type Abstract Method."""
        pass
