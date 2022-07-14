#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Collection Manager."""
from typing import ValuesView

from wlts.collections.feature_collection import FeatureCollection
from wlts.collections.image_collection import ImageCollection


class CollectionFactory:
    """Factory Class for Collection."""

    _factories = {}

    @classmethod
    def register(cls, name, factory):
        """Register a new Collection."""
        cls._factories[name] = factory

    @classmethod
    def make(cls, collection_type: str, collections_info: dict):
        """Factory method to create a collection.

        Args:
            collection_type (str): The collection type to be create.
            collections_info (dict): The collection information.

        Returns:
            collection: A collection object.
        """
        collection = eval(cls._factories[collection_type])(collections_info)

        return collection


class CollectionManager:
    """This is a singleton to manage all collections instances available."""

    _collections = dict()

    _instance = None

    def __new__(cls):
        """Virtually private constructor."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.register_factories()
            cls._instance.load_all()
        return cls._instance

    @staticmethod
    def register_factories() -> None:
        """Register the Collection."""
        CollectionFactory.register('feature_collection', 'FeatureCollection')
        CollectionFactory.register('image_collection', 'ImageCollection')

    def insert(self, collection_type: str, collection_info: dict)-> None:
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

    def collections(self) -> ValuesView:
        """Returns a list with all collections objects."""
        return self._collections.values()

    def load_all(self) -> None:
        """Creates all collection based on json of feature and feature collection."""
        import json
        import os

        from pkg_resources import resource_filename

        feature_collection_dir = resource_filename('wlts', '/json_configs/feature_collection/')
        if os.path.isdir(feature_collection_dir):
            features_files = os.listdir(os.path.dirname(feature_collection_dir))
            for filename in features_files:
                if os.path.isfile(feature_collection_dir + filename):
                    with open(feature_collection_dir + filename, 'r') as f:
                        config_feature = json.loads(f.read())
                        self.insert("feature_collection", config_feature)

        image_collection_dir = resource_filename('wlts', '/json_configs/image_collection/')
        if os.path.isdir(image_collection_dir):
            image_files = os.listdir(os.path.dirname(image_collection_dir))
            for filename in image_files:
                if os.path.isfile(image_collection_dir + filename):
                    with open(image_collection_dir + filename, 'r') as f:
                        config_image = json.loads(f.read())
                        self.insert("image_collection", config_image)


collection_manager = CollectionManager()
