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

from wlts.classificationsys import classification_sys_manager
from wlts.collection import collection_manager
from wlts.schemas import (collections_list, describe_classification_system,
                          describe_collection, list_classification_system,
                          trajectory)
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
        collection_name = request.args['name']
        data = {
            "name": collection_name,
            "description": "string",
            "detail": "",
            "collection_type": "string",
            "resolution_unit": {
                "unit": "string",
                "value": 0
            },
            "time_format": "",
            "period": {
                "start_date": "string",
                "end_date": "string"
            },
            "spatial_extent": {
                "xmin": 0,
                "xmax": 0,
                "ymin": 0,
                "ymax": 0
            },
            "classification_system": "string"
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


@api.route('/list_classification_system')
class ListClassificationSystemController(APIResource):
    """WLTS Trajectory Operation."""

    @require_model(list_classification_system)
    def get(self):
        """Retrieve list of classification offered.

        :returns: Classification list avaliable in server.
        :rtype: dict
        """
        all_classification = classification_sys_manager.get_all_classification_system()

        return jsonify({"classification_system": all_classification})

@api.route('/describe_classification_system')
class DescribeClassificationSystemController(APIResource):
    """WLTS Describe Classification System Operation."""

    @require_model(describe_classification_system)
    def get(self):
        """Retrieves classification system metadata.

        :returns: Collection Description
        :rtype: dict
        """
        classification_sys_name = request.args['name']

        data = {
          "classification_system": classification_sys_name,
          "description": "string",
          "detail": "string",
          "classification_system_class": [
            "string"
          ]
        }


        return jsonify(data)