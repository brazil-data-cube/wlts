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
from pathlib import Path

from wlts.classificationsys import ClassificationSystemClass as Class
from wlts.config import BASE_DIR
from wlts.datasource import datasource_manager

config_folder = Path(BASE_DIR) / 'json-config/'


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
        self.classification_class = Class(classification_class["type"], classification_class["property_name"],
                                                classification_class["property_description"], classification_class["property_id"],
                                                classification_class["class_property_name"])
        self.temporal = temporal
        self.scala = scala
        self.spatial_extent = spatial_extent
        self.period = period

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
            for tl in self.timeline:

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
                    "time": tl
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

    _collenctions = {
        "feature_collection": [],
        "image_collection": []
    }

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

    def insert(self, dsType, collection_info):
        """Insert Collection."""
        collection = CollectionFactory.make(dsType, collection_info)
        self._collenctions[dsType].append(collection)


    def get_collection(self, name):
        """Get Collection."""
        try:
            for c_list in self._collenctions.values():
                for collection in c_list:
                    if collection.get_name() == name:
                        print("Collection found! {} ".format(type(collection)))
                        return collection
        except:
            return None

    def get_all_collection_names(self):
        """Get Name of all collections avaliable."""
        collections_names = list()

        for c_type, c_name in self._collenctions.items():
            for name in c_name:
                collections_names.append(name.get_name())

        return {"collections": collections_names}

    def get_all_collection(self):
        """Get all Collections."""
        all_collection = []

        for c_list in self._collenctions.values():
            for collection in c_list:
                if collection:
                    all_collection.append(collection)
        return all_collection

    def get_collection_name(self, c_type):
        """Get Collection by name."""
        all_collection = []
        for cl in self._collenctions[c_type]:
            if(cl):
                all_collection.append(cl.get_name())
        return all_collection

    def load_all(self):
        """Load all Collection."""
        config_file = config_folder / 'wlts_config.json'

        with config_file.open()  as json_data:

            config = json_loads(json_data.read())

            if "image_collection" in config:
                image_collection = config["image_collection"]
                for img_collection in image_collection:
                    self.insert("image_collection", img_collection)

            if "feature_collection" in config:
                feature_collection = config["feature_collection"]
                for ft_collection in feature_collection:
                    self.insert("feature_collection", ft_collection)

collection_manager = CollectionManager()
