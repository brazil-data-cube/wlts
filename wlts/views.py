#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Views of Web Land Trajectory Service."""
from bdc_core.decorators.validators import require_model
from bdc_core.utils.flask import APIResource
from flask import abort, jsonify, request
from flask_restplus import Namespace
from werkzeug.exceptions import NotFound

from wlts.collections.collection_manager import collection_manager

from . import controller
from .schemas import collections_list, describe_collection, trajectory
from .trajectory import Trajectory, TrajectoryParams

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
        result = {"collections": collection_manager.collection_names()}

        return jsonify(result)


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

        collection = controller.describe_collection(collection_name)

        return jsonify(collection)


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
