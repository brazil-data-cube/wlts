#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Classification System Class."""

from wlts.datasources.ds_manager import datasource_manager


class ClassificationSystemClass:
    """ClassificationSystemClass Class."""

    def __init__(self, **kwargs):
        """Creates a ClassificationSystemClass object."""
        invalid_parameters = set(kwargs) - {"type", "datasource_id", "property_name", "class_property_name",
                                            "class_property_value", 'class_property_id', 'classification_system_name',
                                            'classification_system_id', 'class_property_id'}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self.type = kwargs['type']

        self.property_name = kwargs['property_name']
        self.class_property_name = kwargs['class_property_name']
        self.class_property_value = kwargs['class_property_value']
        self.class_property_id = kwargs['class_property_id']

        self.classification_system_name = kwargs['classification_system_name']
        self.classification_system_id = kwargs['classification_system_id']

        self.datasource = datasource_manager.get_datasource(kwargs['datasource_id'])

    def get_type(self):
        """Get Classification System Class type."""
        return self.type

    def get_property_name(self):
        """Get Classification System Class property name."""
        return self.property_name

    def get_class_property_value(self):
        """Get Classification System Class property value."""
        return self.class_property_value

    def get_class_property_name(self):
        """Get Classification System Class property class name."""
        return self.class_property_name

    def get_class_property_id(self):
        """Get Classification System Class property class id."""
        return self.class_property_id

    def get_class_ds(self):
        """Get DataSource of Classification System."""
        return self.datasource

    def get_classification_system_name(self):
        """Get Classification System Name."""
        return self.classification_system_name

    def get_classification_system_id(self):
        """Get Classification System Id."""
        return self.classification_system_id
