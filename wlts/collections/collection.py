#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Class."""
from abc import ABCMeta, abstractmethod

from wlts.datasources.ds_manager import datasource_manager


class Collection(metaclass=ABCMeta):
    """Abstract class to represent an collection."""

    def __init__(self, name, authority_name, description, detail, datasource_id, dataset_type,
                 classification_class, temporal, scala, spatial_extent, period, is_public):
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
        self.is_public = is_public
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
        args['classification_system_version'] = classification_class.get('classification_system_version', None)

        if classification_class["type"] == 'Self':
            args['property_name'] = None
            args['class_property_name'] = None
            args['class_property_value'] = None

        else:
            args['property_name'] = classification_class["property_name"]
            args['class_property_name'] = classification_class["class_property_name"]
            args['class_property_value'] = classification_class["class_property_value"]

        return ClassificationSystemClass(**args)

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
    def trajectory(self, tj_attr, x, y, start_date, end_date, geometry):
        """Abstract Method to get trajectory.

        Args:
            tj_attr (list): The list of trajectories.
            x (int/float): A longitude value according to EPSG:4326.
            y (int/float): A latitude value according to EPSG:4326.
            start_date (:obj:`str`, optional): The begin of a time interval.
            end_date (:obj:`str`, optional): The begin of a time interval.
            geometry (:obj:`str`, optional): Used to return geometry in trajectory.

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


class ClassificationSystemClass:
    """This class represents a Classification System of a collection."""

    def __init__(self, **kwargs):
        """Creates a ClassificationSystemClass."""
        invalid_parameters = set(kwargs) - {"type", "datasource_id", "property_name", "class_property_name",
                                            "class_property_value", 'class_property_id', 'classification_system_name',
                                            'classification_system_id', 'classification_system_version',
                                            'class_property_id'}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self.type = kwargs['type']

        self.property_name = kwargs['property_name']
        self.class_property_name = kwargs['class_property_name']
        self.class_property_value = kwargs['class_property_value']
        self.class_property_id = kwargs['class_property_id']

        self.classification_system_version = kwargs['classification_system_version']
        self.classification_system_name = kwargs['classification_system_name']
        self.classification_system_id = kwargs['classification_system_id']

        self.datasource = datasource_manager.get_datasource(kwargs['datasource_id'])

    def get_type(self):
        """Return classification system type based on WLTS model."""
        return self.type

    def get_property_name(self):
        """Return classification system property name."""
        return self.property_name

    def get_class_property_value(self):
        """Return classification system property value."""
        return self.class_property_value

    def get_class_property_name(self):
        """Return classification system property class name."""
        return self.class_property_name

    def get_class_property_id(self):
        """Return classification system property class id."""
        return self.class_property_id

    def get_class_ds(self):
        """Return classification system datasource."""
        return self.datasource

    def get_classification_system_version(self):
        """Return classification system name."""
        return self.classification_system_version

    def get_classification_system_name(self):
        """Return classification system name."""
        return self.classification_system_name

    def get_classification_system_id(self):
        """Return classification system id."""
        return self.classification_system_id
