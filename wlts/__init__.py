#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Web Land Trajectory Service."""

import os
from wlts.config import get_settings
from wlts.blueprint import blueprint
from flask import Flask
from flask_cors import CORS

from .version import __version__

def create_app(config_name):

    """
    Creates Brazil Data Cube LUCCWS application from config object
    Args:
        config_name (string|bdc_lucc.config.Config) Config instance
    Returns:
        Flask Application with config instance scope
    """

    internal_app = Flask(__name__)

    with internal_app.app_context():
        internal_app.config.from_object(config_name)
        internal_app.register_blueprint(blueprint)

    return internal_app


app = create_app(get_settings(os.environ.get('ENVIRONMENT', 'DevelopmentConfig')))


CORS(app, resorces={r'/d/*': {"origins": '*'}})

__all__ = ( '__version__', )