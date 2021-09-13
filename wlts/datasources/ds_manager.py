#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
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
    """Factory Class for DataSource."""

    @staticmethod
    def make(ds_type, id, conn_info):
        """Factory method for creates a datasource.

        Args:
            ds_type (str): The datasource type to be create.
            id (str): The datasource identifier.
            conn_info (dict): The datasource connection information.

        .. note::
            New datasources must be add in factorys.

            Ex: factorys = {"POSTGIS": "PostGisDataSource", "WCS": "WCSDataSource", \
                            "WFS": "WFSDataSource", "RASTER FILE": "RasterFileDataSource"}
        """
        factorys = {"WFS": "WFSDataSource", "WCS": "WCSDataSource"}
        datasource = eval(factorys[ds_type])(id, conn_info)
        return datasource


class DataSourceManager:
    """This is a singleton to manage all datasource instances available."""

    _datasources = list()

    _instance = None

    def __new__(cls):
        """Virtually private constructor."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_all()
            return cls._instance
        else:
            return cls._instance

    def get_datasource(self, ds_id):
        """Return a datasource object.

        Args:
            ds_id (str): Identifier of a datasource.

        Returns:
            datasource: A datasource available in the server.

        Raises:
            RuntimeError: If the datasource not found.
        """
        try:
            for ds in self._datasources:
                if ds.get_id == ds_id:
                    return ds
        except ValueError:
            raise RuntimeError(f"Datasource identifier {ds_id} not found in WLTS Datasources!")

    def insert_datasource(self, conn_info):
        """Creates a new datasource and stores in list of datasource.

        Args:
            conn_info (dict): The datasource connection information.
        """
        self._datasources.append(DataSourceFactory.make(conn_info["type"], conn_info["id"], conn_info))

    def load_all(self):
        """Creates all datasource based on json of datasource."""
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
