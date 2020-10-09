#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS DataSource Manager."""
from json import loads as json_loads

import pkg_resources

from .wcs import WCSDataSource
from .wfs import WFSDataSource


class DataSourceFactory:
    """Factory for DataSource."""

    @staticmethod
    def make(ds_type, id, conn_info):
        """Factory method for creates datasource.

        New datasources must be add in factorys.
        Ex: factorys = {"POSTGIS": "PostGisDataSource", "WCS": "WCSDataSource", "WFS": "WFSDataSource",
                        "RASTER FILE": "RasterFileDataSource"}
        """
        factorys = {"WFS": "WFSDataSource", "WCS": "WCSDataSource"}
        datasource = eval(factorys[ds_type])(id, conn_info)
        return datasource


class DataSourceManager:
    """DataSourceManager Class."""

    _datasources = list()

    __instance = None

    def __init__(self):
        """Virtually private constructor."""
        if DataSourceManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DataSourceManager.__instance = self
            DataSourceManager.__instance.load_all()

    @staticmethod
    def get_instance():
        """Static access method."""
        if DataSourceManager.__instance is None:
            DataSourceManager()
        return DataSourceManager.__instance

    def get_datasource(self, ds_id):
        """Get DataSource."""
        try:
            for ds in self._datasources:
                if ds.get_id == ds_id:
                    return ds
        except:
            return None

    def insert_datasource(self, conn_info):
        """Insert DataSource."""
        self._datasources.append(DataSourceFactory.make(conn_info["type"], conn_info["id"], conn_info))

    def load_all(self):
        """Load All DataSources."""
        json_string = pkg_resources.resource_string('wlts', '/json_configs/datasources.json').decode('utf-8')
        config = json_loads(json_string)

        if "datasources" not in config:
            raise ValueError("No datasource in wlts json config file")
        else:
            datasources = config["datasources"]

            for _, datasources_info in datasources.items():
                for ds_info in datasources_info:
                    self.insert_datasource(ds_info)


datasource_manager = DataSourceManager()
