#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
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

    _collections = list()

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
        self._collections.append(collection)

    def get_collection(self, name):
        """Return the collection.

        Args:
            name (str): Identifier (name) of an collection.

        Returns:
            collection: A collection available in the server.

        Raises:
            RuntimeError: If the collection not found.
        """
        try:
            for collection in self._collections:
                if name == collection.get_name():
                    return collection
        except ValueError:
            raise RuntimeError(f"Collection {name} not found!")

    def collection_names(self):
        """Return all available collections.

        Returns:
            list: A list with all collections identifier (name) available in the server.
        """
        collections_names = list()

        for collection in self._collections:
            collections_names.append(collection.get_name())

        return collections_names

    def get_all_collections(self):
        """Returns a list with all collections objects."""
        return self._collections

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
