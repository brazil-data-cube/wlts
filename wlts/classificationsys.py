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

    def __init__(self, type, name, description, id, class_property_name):
        """Creates a ClassificationSystemClass object."""
        self.type = type
        self.name = name
        self.description = description
        self.id = id
        self.class_property_name = class_property_name

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
        """Get ClassificationSystemClass propertyname."""
        return self.class_property_name