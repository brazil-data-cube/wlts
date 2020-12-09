#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Web Land Trajectory Service."""

from flask import Flask
from flask_cors import CORS

from .blueprint import blueprint
from .config import get_settings
from .ext import WLTSDatabase
from .version import __version__


def create_app(config_name='DevelopmentConfig'):
    """Creates Brazil Data Cube WLTS application from config object.

    :param config_name: Config instance.
    :type config_name:string|wlts.config.Config

    :returns: Flask Application with config instance scope.
    """
    app = Flask(__name__)

    conf = get_settings(config_name)
    app.config.from_object(conf)

    with app.app_context():

        CORS(app, resorces={r'/d/*': {"origins": '*'}})

        WLTSDatabase(app)

        app.register_blueprint(blueprint)

    return app


__all__ = ('__version__', 'create_app')
