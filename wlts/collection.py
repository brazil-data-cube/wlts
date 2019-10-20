from abc import ABCMeta, abstractmethod
from json import loads as json_loads
from pathlib import Path
from wlts.datasource import datasource_manager
from wlts.config import BASE_DIR


config_folder = Path(BASE_DIR) / 'json-config/'


class Collection(metaclass=ABCMeta):
    """docstring for ."""

    def __init__(self, name, description, detail, datasource_id):
        self.name = name
        self.description = description
        self.detail = detail
        self.datasource = datasource_manager.get_datasource(datasource_id)

    def get_name(self):
        return self.name

    def get_datasource_id(self):
        return self.datasource_id

    @abstractmethod
    def get_collectiontype(self):
        pass


class FeatureCollection(Collection):
    """ FeatureCollection Class """

    def __init__(self, name, description, detail, datasource_id, type, geom_property, id_property, observations_info):
        super().__init__(name, description, detail, datasource_id)
        self.type = type
        self.geom_property = geom_property
        self.id_property = id_property
        self.observations_info = observations_info

    def get_collectiontype(self):
        return "Feature"


class CollectionFactory:
    @staticmethod
    def make(collection_type, fcinfo):
        factorys = {"feature_collection": "FeatureCollection", "image_collection": "ImageCollection"}

        collection = eval(factorys[collection_type])(fcinfo["name"], fcinfo["description"], fcinfo["detail"],
                                                     fcinfo["datasource_id"],
                                                     fcinfo["type"], fcinfo["geom_property"], fcinfo["id_property"],
                                                     fcinfo["observations_info"])

        return collection


# TODO: singleton
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

            if "image_collection" in config:
                image_collection = config["image_collection"]

            if "feature_collection" in config:
                feature_collection = config["feature_collection"]
                for ft_collection in feature_collection:
                    self.insert("feature_collection", ft_collection)

collection_manager = CollectionManager()
