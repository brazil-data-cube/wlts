#
# This file is part of WLTS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""Views of Web Land Trajectory Service."""
from bdc_auth_client.decorators import oauth2
from flask import Blueprint, jsonify, request
from lccs_db.config import Config as Config_db
from lccs_db.utils import language

from wlts.utils.schemas import (collections_list, describe_collection,
                                trajectory)

from .config import Config
from .controller import WLTS, TrajectoryParams
from .utils.decorators import require_model

bp = Blueprint('wlts', import_name=__name__, url_prefix='/wlts')


@bp.route('/', methods=['GET'])
def root():
    """Retrieve the server version.

    :returns: Server version.
    :rtype: dict
    """
    response = dict(version=Config.WLTS_API_VERSION,
                    application_name= "Web Land Trajectory Service",
                    supported_language=[])

    for _, name in Config_db.I18N_LANGUAGES.items():
        response["supported_language"].append({
            "language": name[0],
            "description": name[1]
        })

    return response


@bp.route('/list_collections', methods=['GET'])
@require_model(collections_list)
@oauth2(required=False)
def list_collections(**kwargs):
    """Retrieve list of collection offered.

    :returns: Collection list available in server.
    :rtype: dict
    """
    return {"collections": WLTS.list_collection(roles=kwargs.get("roles", None))}


@bp.route('/describe_collection', methods=['GET'])
@require_model(describe_collection)
@oauth2(required=False)
def describe_collection(**kwargs):
    """Retrieves collection metadata.

    :returns: Collection Description
    :rtype: dict
    """
    return WLTS.describe_collection(request.args['collection_id'], roles=kwargs.get("roles", None))


@bp.route('/trajectory', methods=['GET'])
@require_model(trajectory)
@oauth2(required=False)
def trajectory(**kwargs):
    """Retrieves collection metadata.

    :returns: Collection Description
    :rtype: dict
    """
    params = TrajectoryParams(**request.args.to_dict())

    return jsonify(WLTS.get_trajectory(params, roles=kwargs.get('roles', None)))
