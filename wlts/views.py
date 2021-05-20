#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Views of Web Land Trajectory Service."""
from bdc_auth_client.decorators import oauth2

from flask import Blueprint, jsonify, request

from wlts.collections.collection_manager import collection_manager
from wlts.utils.schemas import (collections_list, describe_collection,
                                trajectory)

from . import controller
from .config import Config
from .trajectory import WLTS, TrajectoryParams
from .utils.decorators import require_model

bp = Blueprint('wlts', import_name=__name__, url_prefix='/wlts')


@bp.route('/', methods=['GET'])
def root():
    """Retrieve the server version.

    :returns: Server version.
    :rtype: dict
    """
    response = dict()
    response["wlts_version"] = Config.WLTS_API_VERSION

    return response


@bp.route('/list_collections', methods=['GET'])
@require_model(collections_list)
@oauth2(required=False)
def list_collections(roles=[], access_token=""):
    """Retrieve list of collection offered.

    :returns: Collection list available in server.
    :rtype: dict
    """
    return {"collections": WLTS.list_collection(roles=roles)}


@bp.route('/describe_collection', methods=['GET'])
@require_model(describe_collection)
@oauth2(required=False)
def describe_collection(roles=[], access_token=""):
    """Retrieves collection metadata.

    :returns: Collection Description
    :rtype: dict
    """

    return WLTS.describe_collection(request.args['collection_id'], roles=roles)


@bp.route('/trajectory', methods=['GET'])
@require_model(trajectory)
@oauth2(required=True)
def trajectory(**kwargs):
    """Retrieves collection metadata.

    :returns: Collection Description
    :rtype: dict
    """
    params = TrajectoryParams(**request.args.to_dict())

    return jsonify(WLTS.get_trajectory(params, roles=kwargs['roles']))
