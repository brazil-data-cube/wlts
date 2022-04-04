#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Controllers of Web Land Trajectory Service."""
from flask import abort
from werkzeug.exceptions import Forbidden, NotFound

from wlts.collections.collection_manager import collection_manager


class TrajectoryParams:
    """Object wrapper for Trajectory Request Parameters.

    :param properties: trajectory parameter object
    :type properties:dict
    """

    def __init__(self, **properties):
        """Creates a trajectory parameter object."""
        self.collections = properties.get('collections', None)
        if self.collections is not None:
            self.collections = self.collections.split(',')
        self.longitude = float(properties.get('longitude'))
        self.latitude = float(properties.get('latitude'))
        self.start_date = properties.get('start_date', None)
        self.end_date = properties.get('end_date', None)
        self.geometry = properties.get('geometry', None)

    def to_dict(self):
        """Export Trajectory params to Python Dictionary."""
        data = {
            k: v if v is not None else ''
            for k, v in vars(self).items() if not k.startswith('_')
        }
        return data


class WLTS:
    """WLTS Utility."""

    @classmethod
    def list_collection(cls, roles=None):
        """Retrieve a list of collections offered."""
        if not roles:
            roles = []
        collections = list()
        available_collections = collection_manager.collections()

        for collection in available_collections:
            if collection.is_public is True or collection.name in roles:
                collections.append(collection.name)

        return collections

    @classmethod
    def describe_collection(cls, collection_name, roles=None):
        """Retrieve collection description."""
        if not roles:
            roles = []

        cls.check_collection(collection_name, roles)

        collection = collection_manager.collection(collection_name)

        try:
            classification_system = collection.classification_class

            describe = dict()

            describe["classification_system"] = {
                "type": classification_system.type,
                "classification_system_name": classification_system.classification_system_name,
                "classification_system_id": classification_system.classification_system_id,
                "classification_system_version": classification_system.classification_system_version
            }

            describe["name"] = collection.name
            describe["title"] = collection.title
            describe["description"] = collection.description
            describe["detail"] = collection.detail
            describe["is_public"] = collection.is_public
            describe["deprecated"] = collection.deprecated
            describe["collection_type"] = collection.collection_type()
            describe["resolution_unit"] = {
                "unit": collection.get_resolution_unit(),
                "value": float(collection.get_resolution_value())
            }
            describe["period"] = {
                "start_date": collection.get_start_date(),
                "end_date": collection.get_end_date()
            }
            describe["spatial_extent"] = collection.get_spatial_extent()

            describe["datasource"] = {
                "host": collection.host_information,
                "layers": collection.layers_information()
            }

            return describe

        except Exception:
            abort(403, "Error while retrieve collection metadata")

    @classmethod
    def check_collection(cls, collection, roles):
        """Utility to check collection existence in memory and permission."""
        available_collection = collection_manager.collection(collection_id=collection)
        if available_collection is None:
            raise NotFound(f"Collection {collection} not found!")
        if available_collection.is_public is False and available_collection.name not in roles:
            raise Forbidden('Forbidden')

    @staticmethod
    def get_collections(names):
        """Retrieves collections."""
        return collection_manager.find_collections(names)

    @classmethod
    def get_trajectory(cls, ts_params: TrajectoryParams, roles=None):
        """
        Retrieves trajectory object.

        :param ts_params: WLTS Request trajectory parameters
        :type ts_params: TrajectoryParams

        :returns: Trajectory.
        :rtype: dict

        """
        if not roles:
            roles = []
        for collection in ts_params.collections:
            cls.check_collection(collection, roles)

        # Retrieves the collections that matches the Trajectory collections name arguments
        collections = cls.get_collections(ts_params.collections)

        tj_attr = []
        for collection in collections:
            collection.trajectory(tj_attr, ts_params.longitude, ts_params.latitude, ts_params.start_date,
                                  ts_params.end_date, ts_params.geometry)

        trajectory_result = sorted(tj_attr, key=lambda k: k['date'])

        return {
            "query": ts_params.to_dict(),
            "result": {
                "trajectory": trajectory_result
            }
        }
