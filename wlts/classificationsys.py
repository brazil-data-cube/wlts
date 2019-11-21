#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Classification System Module for WLTS."""
from json import loads as json_loads
from pathlib import Path

from wlts.config import BASE_DIR

config_folder = Path(BASE_DIR) / 'json-config/'


class ClassificationSystem:
    """ClassificationSystem Class."""

    def __init__(self, classification_sys):
        """Creates a ClassificationSystem object."""
        self.id = classification_sys["id"]
        self.name = classification_sys["name"]
        self.authority_name = classification_sys["authority_name"]
        self.description = classification_sys["description"]
        self.detail = classification_sys["detail"]
        self.version = classification_sys["version"]

    def get_classification_sys_id(self):
        """Get Classification System id."""
        return self.id

    def get_classification_sys_name(self):
        """Get Classification System name."""
        return self.name

    def get_classification_sys_authority_name(self):
        """Get Classification System authority name."""
        return self.authority_name

    def get_classification_sys_description(self):
        """Get Classification System description."""
        return self.description

    def get_classification_sys_detail(self):
        """Get Classification System detail."""
        return self.detail

    def get_classification_sys_version(self):
        """Get Classification System version."""
        return self.version


class ClassificationSystemClass:
    """ClassificationSystemClass Class."""

    def __init__(self, classification_sys_id, type, name, description, id, class_property_name):
        """Creates a ClassificationSystemClass object."""
        self.classification_sys_id = classification_sys_id
        self.type = type
        self.name = name
        self.description = description
        self.id = id
        self.class_property_name = class_property_name

    def get_classification_sys(self):
        """Return ClassificationSystem by id."""
        csm = ClassificationSystemManager.getInstance()
        return csm.get_classification_sys_by_id(self.classification_sys_id)

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


class ClassificationSystemManager:
    """ClassificationSystemManager Class."""

    _classification_sys = []

    __instance = None

    def __init__(self):
        """Virtually private constructor."""
        if ClassificationSystemManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ClassificationSystemManager.__instance = self
            ClassificationSystemManager.__instance.load_all()

    @staticmethod
    def getInstance():
        """Static access method."""
        if ClassificationSystemManager.__instance == None:
            ClassificationSystemManager()
        return ClassificationSystemManager.__instance

    def insert(self, classification_sys):
        """Insert ClassificationSystem."""
        classification_sys_obj = ClassificationSystem(classification_sys)
        self._classification_sys.append(classification_sys_obj)

    def get_name_by_id(self, id):
        """Get ClassificationSystem name by id."""
        for cls_sys in self._classification_sys:
            if (id == cls_sys.get_classification_sys_id()):
                return cls_sys.get_classification_sys_name()

    def get_classification_sys_by_id(self, id):
        """Get ClassificationSystem by id."""
        for cls_sys in self._classification_sys:
            if (id == cls_sys.get_classification_sys_id()):
                return cls_sys

    def get_all_classification_system(self):
        """Get all ClassificationSystem."""
        all_classification_sys = []

        for classification_syst in self._classification_sys:
            all_classification_sys.append(classification_syst.get_classification_sys_name())

        return all_classification_sys

    def load_all(self):
        """Load all ClassificationSystem."""
        config_file = config_folder / 'wlts_config.json'

        with config_file.open()  as json_data:

            config = json_loads(json_data.read())

            if ("classification_system" in config):
                classification_system = config["classification_system"]
                for classification_sys in classification_system:
                    self.insert(classification_sys)
            else:
                raise ValueError("No classification_system in json config file")


classification_sys_manager = ClassificationSystemManager()
