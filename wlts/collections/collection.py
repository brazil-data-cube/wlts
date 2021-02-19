#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Class."""
from abc import ABCMeta, abstractmethod

from wlts.collections.class_system import ClassificationSystemClass as Class
from wlts.datasources.ds_manager import datasource_manager


class Collection(metaclass=ABCMeta):
    """Abstract class to represent an collection."""

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
        """Creates a Classification System for Collection.

        Args:
            classification_class (dict): The classification system information.

        Returns:
            Class: The classification system class.

        """
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
        """Return the collection name."""
        return self.name

    def get_datasource_id(self):
        """Return the collection datasource identifier (id)."""
        return self.datasource.get_id()

    def get_datasource(self):
        """Return datasource of the collection."""
        return self.datasource

    def get_resolution_unit(self):
        """Return the collection resolution unit."""
        return self.temporal["resolution"]["unit"]

    def get_resolution_value(self):
        """Return the collection resolution value."""
        return self.temporal["resolution"]["value"]

    def get_spatial_extent(self):
        """Return the collection spatial extent."""
        return self.spatial_extent

    def get_start_date(self):
        """Return the collection start date."""
        return self.period["start_date"]

    def get_end_date(self):
        """Return the collection end_date."""
        return self.period["end_date"]

    @abstractmethod
    def trajectory(self, tj_attr, x, y, start_date, end_date):
        """Abstract Method to get trajectory.

        Args:
            tj_attr (list): The list of trajectories.
            x (int/float): A longitude value according to EPSG:4326.
            y (int/float): A latitude value according to EPSG:4326.
            start_date (:obj:`str`, optional): The begin of a time interval.
            end_date (:obj:`str`, optional): The begin of a time interval.

         Returns:
            list: A trajectory object as a list.
        """
        pass

    @abstractmethod
    def collection_type(self):
        """Abstract Method to get collections type.

        Returns:
            collection_type (str): A string that represents a collection type.
        """
        pass
