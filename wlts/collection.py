from abc import ABCMeta, abstractmethod
from json import loads as json_loads
from pathlib import Path
from wlts.datasource import datasource_manager
from wlts.config import BASE_DIR


config_folder = Path(BASE_DIR) / 'json-config/'


class Collection(metaclass=ABCMeta):
    """docstring for ."""

    def __init__(self, name, authority_name, description, detail, datasource_id, dataset_type,
                 classification_class, temporal, scala, spatial_extent):
        self.name = name
        self.authority_name = authority_name
        self.description = description
        self.detail = detail
        self.datasource = datasource_manager.get_datasource(datasource_id),
        self.dataset_type = dataset_type
        self.classification_class = classification_class
        self.temporal = temporal
        self.scala = scala
        self.spatial_extent = spatial_extent


    def get_name(self):
        return self.name

    def get_datasource_id(self):
        return self.datasource.get_id()

    def get_datasource(self):
        return self.datasource

    @abstractmethod
    def get_collectiontype(self):
        pass


class FeatureCollection(Collection):
    """ FeatureCollection Class """

    def __init__(self, collections_info):
        super().__init__(collections_info["name"], collections_info["authority_name"], collections_info["description"],
                         collections_info["detail"], collections_info["datasource_id"], collections_info["dataset_type"],
                         collections_info["classification_class"], collections_info["temporal"],
                         collections_info["scala"], collections_info["spatial_extent"])
        self.feature_type = collections_info["feature_type"]
        self.feature_id_property = collections_info["feature_id_property"]
        self.geom_property = collections_info["geom_property"]
        self.observations_properties = collections_info["observations_properties"]

    def get_collectiontype(self):
        return "Feature"


class CollectionFactory:
    @staticmethod
    def make(collection_type, collections_info):
        factorys = {"feature_collection": "FeatureCollection", "image_collection": "ImageCollection"}


        collection = eval(factorys[collection_type])(collections_info)

        return collection

class CollectionManager:
    """docstring for ."""

    _collenctions = {
        "feature_collection": [],
        "image_collection": []
    }

    __instance = None

    def __init__(self):
        """ Virtually private constructor. """
        if CollectionManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            CollectionManager.__instance = self
            CollectionManager.__instance.load_all()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if CollectionManager.__instance == None:
            CollectionManager()
        return CollectionManager.__instance

    def insert(self, dsType, collection_info):
        collection = CollectionFactory.make(dsType, collection_info)
        self._collenctions[dsType].append(collection)

    def get_collection(self, name):
        for c_list in self._collenctions.values():
            for collection in c_list:
                if collection.get_name() == name:
                    return collection
        return None

    def get_all_collection_names(self):
        all_collection = {
            "feature_collection": [],
            "image_collection": []
        }
        for c_key, c_value in self._collenctions.items():
            for collection_v in c_value:
                if (collection_v):
                    all_collection[c_key].append(collection_v.get_name())
        return all_collection

    def get_collection_name(self, c_type):
        all_collection = []
        for cl in self._collenctions[c_type]:
            if(cl):
                all_collection.append(cl.get_name())
        return all_collection

    def load_all(self):

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
