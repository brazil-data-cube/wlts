#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Controllers of Web Land Trajectory Service."""
from bdc_core.decorators.validators import require_model
from bdc_core.utils.flask import APIResource
from flask import jsonify, request
from flask_restplus import Namespace

from wlts.collection import collection_manager
from wlts.schemas import collections_list, describe_collection, trajectory
from wlts.trajectory import Trajectory, TrajectoryParams

api = Namespace('wlts', description='status')


@api.route('/list_collections')
class ListCollectionsController(APIResource):
    """WLTS ListCollections Operation."""

    @require_model(collections_list)
    def get(self):
        """Retrieve list of collection offered.

        :returns: Collection list avaliable in server.
        :rtype: dict
        """
        return jsonify(collection_manager.get_all_collection_names())


@api.route('/describe_collection')
class DescribeCollection(APIResource):
    """WLTS DescribeCollection Operation."""

    @require_model(describe_collection)
    def get(self):
        """Retrieves collection metadata.

        :returns: Collection Description
        :rtype: dict
        """
        collection_name = request.args['collection_id']

        collection = collection_manager.get_collection(collection_name)

        data = {
            "name": collection.name,
            "description": collection.description,
            "detail": collection.detail,
            "collection_type": collection.get_collectiontype(),
            "resolution_unit": {
                "unit": collection.get_resolution_unit(),
                "value": collection.get_resolution_value()
            },
            "period": {
                "start_date": collection.get_start_date(),
                "end_date": collection.get_end_date()
            },
            "spatial_extent": collection.get_spatial_extent()
        }

        return jsonify(data)


@api.route('/trajectory')
class TrajectoryController(APIResource):
    """WLTS Trajectory Operation."""

    @require_model(trajectory)
    def get(self):
        """Retrieves collection metadata.

        :returns: Collection Description
        :rtype: dict
        """
        params = TrajectoryParams(**request.args.to_dict())

        return jsonify(Trajectory.get_trajectory(params))
