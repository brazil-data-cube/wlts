#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS DataSource Manager."""
import pkg_resources
from json import loads as json_loads

from .wfs import WFSDataSource
from .wcs import WCSDataSource

class DataSourceFactory:
    """Factory for DataSource."""

    @staticmethod
    def make(dsType, id, connInfo):
        """Factory method for creates datasource."""
        # factorys = {"POSTGIS": "PostGisDataSource", "WCS": "WCSDataSource", "WFS": "WFSDataSource",
        #             "RASTER FILE": "RasterFileDataSource"}
        #TODO colocar todos
        factorys = { "WFS": "WFSDataSource", "WCS": "WCSDataSource"}
        datasource = eval(factorys[dsType])(id, connInfo)
        return datasource


class DataSourceManager:
    """DataSourceManager Class."""

    _datasources = list()

    __instance = None

    def __init__(self):
        """Virtually private constructor."""
        if DataSourceManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DataSourceManager.__instance = self
            DataSourceManager.__instance.load_all()

    @staticmethod
    def getInstance():
        """Static access method."""
        if DataSourceManager.__instance == None:
            DataSourceManager()
        return DataSourceManager.__instance

    def get_datasource(self, ds_id):
        """Get DataSource."""
        try:
            for ds in self._datasources:
                if (ds.get_id == ds_id):
                    return ds
        except:
            return None

    def insert_datasource(self, dsType, connInfo):
        """Insert DataSource."""
        self._datasources.append(DataSourceFactory.make(connInfo["type"], connInfo["id"], connInfo))

    def load_all(self):
        """Load All DataSources."""
        json_string = pkg_resources.resource_string('wlts', '/json_configs/datasources.json').decode('utf-8')
        config = json_loads(json_string)

        if "datasources" not in config:
            raise ValueError("No datasource in wlts json config file")
        else:
            datasources = config["datasources"]

            for dstype, datasources_info in datasources.items():
                for ds_info in datasources_info:
                    self.insert_datasource(dstype, ds_info)


datasource_manager = DataSourceManager()
