#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Manager."""
from json import loads as json_loads

import pkg_resources

from wlts.collections.feature_collection import FeatureCollection
from wlts.collections.image_collection import ImageCollection


class CollectionFactory:
    """Factory Class for Collection."""

    @staticmethod
    def make(collection_type, collections_info):
        """Factory method to creates a collection.

        Args:
            collection_type (str): The collection type to be create.
            collections_info (dict): The collection information.

        Returns:
            collection: A collection object.
        """
        factorys = {"feature_collection": "FeatureCollection", "image_collection": "ImageCollection"}

        collection = eval(factorys[collection_type])(collections_info)

        return collection


class CollectionManager:
    """This is a singleton to manage all collections instances available."""

    _collections = dict()

    __instance = None

    def __init__(self):
        """Virtually private constructor."""
        if CollectionManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CollectionManager.__instance = self
            CollectionManager.__instance.load_all()

    @staticmethod
    def get_instance():
        """Static access method."""
        if CollectionManager.__instance is None:
            CollectionManager()
        return CollectionManager.__instance

    def insert(self, collection_type, collection_info):
        """Method to creates a new collection and stores in list of collections.

        Args:
            collection_type (str): The collection type to be create.
            collection_info (dict): The collection information.
        """
        collection = CollectionFactory.make(collection_type, collection_info)
        self._collections[collection.name] = collection

    def collection(self, collection_id: str):
        """Return the collection.

        Args:
            collection_id (str): Identifier (name) of an collection.

        Returns:
            collection: A collection available in the server.
        """
        if collection_id in self._collections.keys():
            return self._collections[collection_id]

    def find_collections(self, names: list):
        """Return list of collections.

        Args:
            names (list): A list with the collections names.

        Returns:
            collections: All collection available in the server.
        """
        return [self._collections[x] for x in names]

    def collection_names(self):
        """Return all available collections.

        Returns:
            list: A list with all collections identifier (name) available in the server.
        """
        return list(self._collections.keys())

    def collections(self):
        """Returns a list with all collections objects."""
        return self._collections.values()

    def load_all(self):
        """Creates all collection based on json of image and feature collection."""
        json_string_feature = pkg_resources.resource_string('wlts', '/json_configs/feature_collection.json').decode(
            'utf-8')

        json_string_image = pkg_resources.resource_string('wlts', '/json_configs/image_collection.json').decode('utf-8')

        config_feature = json_loads(json_string_feature)
        config_image = json_loads(json_string_image)

        if "feature_collection" in config_feature:
            feature_collection = config_feature["feature_collection"]
            for ft_collection in feature_collection:
                self.insert("feature_collection", ft_collection)

        if "image_collection" in config_image:
            image_collection = config_image["image_collection"]
            for img_collection in image_collection:
                self.insert("image_collection", img_collection)


collection_manager = CollectionManager()
