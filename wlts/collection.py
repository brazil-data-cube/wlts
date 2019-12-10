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

from wlts.classificationsys import ClassificationSystemClass as ClassSystem
from wlts.config import BASE_DIR
from wlts.datasource import datasource_manager

config_folder = Path(BASE_DIR) / 'json-config/'


class Collection(metaclass=ABCMeta):
    """Abstract Collection Class."""

    def __init__(self, name, authority_name, description, detail, datasource_id, dataset_type,
                 classification_class, temporal, scala, spatial_extent):
        """Creates Collection."""
        self.name = name
        self.authority_name = authority_name
        self.description = description
        self.detail = detail
        self.datasource = datasource_manager.get_datasource(datasource_id)
        self.dataset_type = dataset_type
        self.classification_class = ClassSystem(classification_class["classification_system_id"],
                                                classification_class["type"], classification_class["property_name"],
                                                classification_class["property_description"], classification_class["property_id"],
                                                classification_class["class_property_name"])
        self.temporal = temporal
        self.scala = scala
        self.spatial_extent = spatial_extent

        # print("\nInicializando Collections\n")

    def get_name(self):
        """Get Collection Name."""
        return self.name

    def get_datasource_id(self):
        """Get Collection id."""
        return self.datasource.get_id()

    def get_datasource(self):
        """Get Collection DataSource."""
        return self.datasource


    @abstractmethod
    def get_collectiontype(self):
        """Get Collection Type Abstract Method."""
        pass

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
                         collections_info["scala"], collections_info["spatial_extent"])
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

            # print("Pegando trajectory for obs {}".format(obs))

            result = ds.get_trajectory(self.feature_type, self.temporal,x, y, obs, self.geom_property,
                                   self.classification_class, start_date, end_date)

            if(result):
                # print("Result Type {}".format(type(result[0])))
                trj = {
                    "collection_name": self.get_name(),
                    "classification_class": result[0],
                    "data": str(result[1])
                }

                tj_attr.append(trj)

        # return tj_attr


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
        print("Inicializando CollectionManager")

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
        """Get all Collections Name."""
        all_collection = {
            "feature_collection": [],
            "image_collection": []
        }
        for c_key, c_value in self._collenctions.items():
            for collection_v in c_value:
                if (collection_v):
                    all_collection[c_key].append(collection_v.get_name())
        return all_collection

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

            # if "image_collection" in config:
            #     image_collection = config["image_collection"]

            if "feature_collection" in config:
                feature_collection = config["feature_collection"]
                for ft_collection in feature_collection:
                    self.insert("feature_collection", ft_collection)

collection_manager = CollectionManager()
