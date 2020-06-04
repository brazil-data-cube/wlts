#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Python Collection Class and methods for WLTS."""
from abc import ABCMeta, abstractmethod
from json import loads as json_loads

import pkg_resources

from .classificationsys import ClassificationSystemClass as Class
from .datasource import datasource_manager


class Collection(metaclass=ABCMeta):
    """Abstract Collection Class."""

    def __init__(self, name, authority_name, description, detail, datasource_id, dataset_type,
                 classification_class, temporal, scala, spatial_extent, period):
        """Creates Collection."""
        self.name = name
        self.authority_name = authority_name
        self.description = description
        self.detail = detail
        self.datasource = datasource_manager.get_datasource(datasource_id)
        self.dataset_type = dataset_type
        self.classification_class = self.init_classification_system(classification_class)
        self.temporal = temporal
        self.scala = scala
        self.spatial_extent = spatial_extent
        self.period = period

    def init_classification_system(self, classification_class):
        """Creates Class."""
        args = dict()

        args['type'] = classification_class["type"]
        args['name'] = classification_class["property_name"]
        args['class_name'] = classification_class["class_property_name"]
        args['id'] = classification_class["property_id"]
        args['code'] = None
        args['description'] = None
        args['base'] = None

        if 'property_code' in classification_class:
            args['code'] = classification_class["property_code"]

        if 'property_description' in classification_class:
            args['description'] = classification_class["property_description"]

        if 'property_base' in classification_class:
            args['base'] = classification_class["property_base"]

        return Class(**args)

    def get_name(self):
        """Get Collection Name."""
        return self.name

    def get_datasource_id(self):
        """Get Collection id."""
        return self.datasource.get_id()

    def get_datasource(self):
        """Get Collection DataSource."""
        return self.datasource

    def get_resolution_unit(self):
        """Get Collection Time resolution unit."""
        return self.temporal["resolution"]["unit"]

    def get_resolution_value(self):
        """Get Collection Time resolution value."""
        return self.temporal["resolution"]["value"]

    def get_spatial_extent(self):
        """Get Collection Spatial_extent."""
        return self.spatial_extent

    def get_start_date(self):
        """Get Collection start_date."""
        return self.period["start_date"]

    def get_end_date(self):
        """Get Collection end_date."""
        return self.period["end_date"]

    @abstractmethod
    def trajectory(self, tj_attr, x, y, start_date, end_date):
        """Get Trajectory Type Abstract Method."""
        pass


class FeatureCollection(Collection):
    """FeatureCollection Class."""

    def __init__(self, collections_info):
        """Creates FeatureCollection."""
        super().__init__(collections_info["name"], collections_info["authority_name"], collections_info["description"],
                         collections_info["detail"], collections_info["datasource_id"], collections_info["dataset_type"],
                         collections_info["classification_class"], collections_info["temporal"],
                         collections_info["scala"], collections_info["spatial_extent"], collections_info["period"])
        self.feature_type = collections_info["feature_type"]
        self.feature_id_property = collections_info["feature_id_property"]
        self.geom_property = collections_info["geom_property"]
        self.observations_properties = collections_info["observations_properties"]

    def get_collectiontype(self):
        """Get Collection Feature Type."""
        return "Feature"


    def trajectory(self, tj_attr, x, y, start_date, end_date):
        """Get Trajectory."""
        ds = self.get_datasource()

        for obs in self.observations_properties:

            args = {
                "feature_type": self.feature_type,
                "temporal": self.temporal,
                "x": x,
                "y": y,
                "obs": obs,
                "geom_property": self.geom_property,
                "classification_class": self.classification_class,
                "start_date": start_date,
                "end_date" : end_date
            }

            result = ds.get_trajectory(**args)

            if(result):
                trj = {
                    "collection": self.get_name(),
                    "class": result[0],
                    "date": str(result[1])
                }

                tj_attr.append(trj)

class ImageCollection(Collection):
    """ImageCollection Class."""

    def __init__(self, collections_info):
        """Creates ImageCollection."""
        super().__init__(collections_info["name"], collections_info["authority_name"], collections_info["description"],
                         collections_info["detail"], collections_info["datasource_id"],
                         collections_info["dataset_type"],
                         collections_info["classification_class"], collections_info["temporal"],
                         collections_info["scala"], collections_info["spatial_extent"],collections_info["period"])
        self.image = collections_info["image"]
        self.grid = collections_info["grid"]
        self.spatial_ref_system = collections_info["spatial_reference_system"]
        self.attributes_properties = collections_info["attributes_properties"]
        self.timeline = collections_info["timeline"]

    def get_collectiontype(self):
        """Get Collection Image Type."""
        return "Image"

    def trajectory(self, tj_attr, x, y, start_date, end_date):
        """Get Trajectory."""
        ds = self.get_datasource()

        for obs in self.attributes_properties:
            for time in self.timeline:
                args = {
                    "image": self.image,
                    "temporal": self.temporal,
                    "x": x,
                    "y": y,
                    "attribute": obs,
                    "grid": self.grid,
                    "srid" : self.spatial_ref_system["srid"],
                    "classification_class": self.classification_class,
                    "start_date": start_date,
                    "end_date": end_date,
                    "time": time
                }

                result = ds.get_trajectory(**args)

                if (result):

                    trj = {
                        "collection": self.get_name(),
                        "class": result[0],
                        "date": str(result[1])
                    }

                    tj_attr.append(trj)



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
        json_string = pkg_resources.resource_string(__name__, '/json-config/wlts_config.json').decode('utf-8')

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
