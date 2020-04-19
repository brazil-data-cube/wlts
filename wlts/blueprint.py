#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Brazil Data Cube Main Blueprint."""
from flask import Blueprint
from flask_restplus import Api

from .controller import api as wlts_ns

blueprint = Blueprint('wlts', __name__)

api = Api(blueprint, doc='')

api.add_namespace(wlts_ns)
