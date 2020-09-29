#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Abstract Class."""

from wlts.datasources.ds_manager import datasource_manager

class ClassificationSystemClass:
    """ClassificationSystemClass Class."""

    def __init__(self, **kwargs):
        """Creates a ClassificationSystemClass object."""
        invalid_parameters = set(kwargs) - {"type", "name", "class_name", "value", "datasource_id", 'class_system'}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self.type = kwargs['type']

        self.name = kwargs['name']
        self.value = kwargs['value']
        self.class_name = kwargs['class_name']

        self.class_system = None

        if 'class_system' in kwargs:
            self.class_system = kwargs['class_system']

        if self.type == 'Self':
            self.datasource = None

        else:
            self.datasource = datasource_manager.get_datasource(kwargs['datasource_id'])

    def get_type(self):
        """Get ClassificationSystemClass type."""
        return self.type

    def get_name(self):
        """Get ClassificationSystemClass name."""
        return self.name

    def get_value(self):
        """Get ClassificationSystemClass id."""
        return self.value

    def get_class_property_name(self):
        """Get ClassificationSystemClass property_name."""
        return self.class_name

    def get_class_ds(self):
        """Get DataSource of Classification System."""
        return self.datasource

    def get_class_system(self):
        """Get DataSource of Classification System."""
        return self.class_system

