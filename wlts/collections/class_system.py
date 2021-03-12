#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Classification System Class."""

from wlts.datasources.ds_manager import datasource_manager


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
