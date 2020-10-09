#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Class."""
from abc import ABCMeta, abstractmethod

from wlts.collections.class_system import ClassificationSystemClass as Class
from wlts.datasources.ds_manager import datasource_manager


class Collection(metaclass=ABCMeta):
    """Abstract Collection Class."""

    def __init__(self, name, authority_name, description, detail, datasource_id, dataset_type,
                 classification_class, temporal, scala, spatial_extent, period):
        """Create Collection."""
        self.name = name
        self.authority_name = authority_name
        self.description = description
        self.detail = detail
        self.dataset_type = dataset_type
        self.temporal = temporal
        self.scala = scala
        self.spatial_extent = spatial_extent
        self.period = period
        self.classification_class = self.create_classification_system(classification_class)

        self.datasource = datasource_manager.get_datasource(datasource_id)

    @staticmethod
    def create_classification_system(classification_class):
        """Creates Class."""
        args = dict()

        args['type'] = classification_class["type"]
        args['datasource_id'] = classification_class["datasource_id"]
        args['class_property_id'] = classification_class.get('class_property_id', None)
        args['classification_system_name'] = classification_class.get('classification_system_name', None)
        args['classification_system_id'] = classification_class.get('classification_system_id', None)

        if classification_class["type"] == 'Self':
            args['property_name'] = None
            args['class_property_name'] = None
            args['class_property_value'] = None

        else:
            args['property_name'] = classification_class["property_name"]
            args['class_property_name'] = classification_class["class_property_name"]
            args['class_property_value'] = classification_class["class_property_value"]

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
