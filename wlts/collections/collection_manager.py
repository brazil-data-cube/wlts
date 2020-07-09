#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Manager."""
import pkg_resources
from json import loads as json_loads

from wlts.collections.feature_collection import FeatureCollection
from wlts.collections.image_collection import ImageCollection


class CollectionFactory:
    """Factory Class for Collection."""

    @staticmethod
    def make(collection_type, collections_info):
        """Factory method creates Collection."""
        factorys = {"feature_collection": "FeatureCollection", "image_collection": "ImageCollection"}

        collection = eval(factorys[collection_type])(collections_info)

        return collection

class CollectionManager:
    """CollectionManager Class."""

    _collections = list()

    __instance = None

    def __init__(self):
        """Virtually private constructor."""
        if CollectionManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CollectionManager.__instance = self
            CollectionManager.__instance.load_all()

    @staticmethod
    def getInstance():
        """Static access method."""
        if CollectionManager.__instance == None:
            CollectionManager()
        return CollectionManager.__instance

    def insert(self, collectionType, collection_info):
        """Insert Collection."""
        collection = CollectionFactory.make(collectionType, collection_info)
        self._collections.append(collection)


    def get_collection(self, name):
        """Get Collection."""
        try:
            for collection in self._collections:
                if name == collection.get_name():
                    return collection
        except:
            return None

    def collection_names(self):
        """Get Name of all collections avaliable."""
        collections_names = list()

        for collection in self._collections:
            collections_names.append(collection.get_name())

        return collections_names

    def get_all_collections(self):
        """Get all Collections."""
        return self._collections

    def load_all(self):
        """Load all Collection."""
        json_string = pkg_resources.resource_string('wlts', '/json_configs/collections.json').decode('utf-8')

        config = json_loads(json_string)

        if "feature_collection" in config:
            feature_collection = config["feature_collection"]
            for ft_collection in feature_collection:
                self.insert("feature_collection", ft_collection)

        if "image_collection" in config:
            image_collection = config["image_collection"]
            for img_collection in image_collection:
                self.insert("image_collection", img_collection)

collection_manager = CollectionManager()
