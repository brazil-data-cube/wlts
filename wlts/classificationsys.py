#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Class Module for WLTS."""

class ClassificationSystemClass:
    """ClassificationSystemClass Class."""

    def __init__(self, **kwargs):
        """Creates a ClassificationSystemClass object."""
        invalid_parameters = set(kwargs) - {"type", "name", "class_name", "id", "base", "code", "description"}

        if invalid_parameters:
            raise AttributeError('invalid parameter(s): {}'.format(invalid_parameters))

        self.type = kwargs['type']
        self.name = kwargs['name']
        self.id =  kwargs['id']
        self.class_name = kwargs['class_name']
        self.base = kwargs['base']
        self.code = kwargs['code']
        self.description = kwargs['description']

    def get_type(self):
        """Get ClassificationSystemClass type."""
        return self.type

    def get_name(self):
        """Get ClassificationSystemClass name."""
        return self.name

    def get_description(self):
        """Get ClassificationSystemClass description."""
        return self.description

    def get_id(self):
        """Get ClassificationSystemClass id."""
        return self.id

    def get_class_property_name(self):
        """Get ClassificationSystemClass property_name."""
        return self.class_name

    def get_base(self):
        """Get ClassificationSystemClass base : Workspace or schema."""
        return self.base

    def get_code(self):
        """Get ClassificationSystemClass workspace."""
        return self.code