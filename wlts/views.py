#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Views of Web Land Trajectory Service."""
from bdc_core.decorators.validators import require_model
from flask import Blueprint, jsonify, request

from wlts.collections.collection_manager import collection_manager

from . import controller
from .schemas import collections_list, describe_collection, trajectory
from .trajectory import Trajectory, TrajectoryParams

bp = Blueprint('wlts', import_name=__name__, url_prefix='/wlts')


@bp.route('/list_collections', methods=['GET'])
@require_model(collections_list)
def list_collections():
    """Retrieve list of collection offered.

    :returns: Collection list avaliable in server.
    :rtype: dict
    """
    result = {"collections": collection_manager.collection_names()}

    return jsonify(result)


@bp.route('/describe_collection', methods=['GET'])
@require_model(describe_collection)
def describe_collection():
    """Retrieves collection metadata.

    :returns: Collection Description
    :rtype: dict
    """
    collection_name = request.args['collection_id']

    collection = controller.describe_collection(collection_name)

    return jsonify(collection)


@bp.route('/trajectory', methods=['GET'])
@require_model(trajectory)
def trajectory():
    """Retrieves collection metadata.

    :returns: Collection Description
    :rtype: dict
    """
    params = TrajectoryParams(**request.args.to_dict())

    return jsonify(Trajectory.get_trajectory(params))