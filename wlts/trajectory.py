#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""This class implements a  for WLTS."""
from werkzeug.exceptions import BadRequest, NotFound

from .collection import collection_manager


class TrajectoryParams:
    """Object wrapper for Trajectory Request Parameters.

    :param properties: trajectory parameter object
    :type properties:dict
    """

    def __init__(self, **properties):
        """Creates a trajectory parameter object."""
        self.collections = properties.get('collections').split(',') if properties.get('collections') else None
        self.longitude = float(properties.get('longitude'))
        self.latitude = float(properties.get('latitude'))
        self.start_date = properties.get('start_date') if properties.get('start_date') else None
        self.end_date = properties.get('end_date') if properties.get('end_date') else None

    def to_dict(self):
        """Export Trajectory params to Python Dictionary."""
        return {
            k: v
            for k, v in vars(self).items() if not k.startswith('_')
            }


class Trajectory:
    """Trajectory Class.

    :param cls: instance ...
    """

    @classmethod
    def list_collection(cls):
        """Creates a trajectory parameter object."""
        return collection_manager.get_all_collection_names()

    @classmethod
    def check_collection(cls, collection):
        """Utility to check collection existence in memory."""
        # print(collection)
        # print(cls.list_collection())
        if collection not in cls.list_collection():
            raise NotFound('Collection "{}" not found'.format(collection))

    @staticmethod
    def get_collections(ts_params):
        """Retrieves collections."""
        features = []
        try:

            for collections_name in ts_params.collections:
                features.append(collection_manager.get_collection(collections_name))

            return features

        except RuntimeError:
            raise BadRequest('No Collection found')

    @classmethod
    def get_trajectory(cls, ts_params: TrajectoryParams):
        """
        Retrieves trajectory object.

        :param ts_params: WLTS Request trajectory parameters
        :type ts_params: TrajectoryParams

        :returns: Trajectory.
        :rtype: dict

        """
        if (ts_params.collections):

            # Validate collection existence
            for collection in ts_params.collections:
                cls.check_collection(collection)

            collections = cls.get_collections(ts_params)
        else:
            collections = collection_manager.get_all_collection()

        # Retrieves the collections that matches the Trajectory collections name arguments

        tj_attr = []

        for collection in collections:
            collection.trajectory(tj_attr, ts_params.longitude, ts_params.latitude, ts_params.start_date,
                                  ts_params.end_date)

        newtraj = sorted(tj_attr, key=lambda k: k['date'])

        return {
            "query": ts_params.to_dict(),
            "result": {
                "trajectory": newtraj
            }

        }
