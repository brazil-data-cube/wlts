"""
Brazil Data Cube Main Blueprint
This file configures application routes, adding namespaces
into global API object
"""

from flask import Blueprint
from flask_restplus import Api
from wlts.controller import api as wlts_ns


blueprint = Blueprint('wlts', __name__)

api = Api(blueprint, doc='')

api.add_namespace(wlts_ns)
