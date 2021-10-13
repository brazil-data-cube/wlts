#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Web Land Trajectory Service."""

import os

from flask import Flask
from werkzeug.exceptions import HTTPException, InternalServerError

from .config import get_settings
from .version import __version__


def create_app():
    """Creates Brazil Data Cube WLTS application from config object.

    :returns: Flask Application with config instance scope.
    """
    app = Flask(__name__)

    conf = config.get_settings(os.environ.get('WLTS_ENVIRONMENT', 'DevelopmentConfig'))

    app.config.from_object(conf)

    setup_app(app)

    setup_wlts_managers()

    return app


def setup_app(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle exceptions."""
        if isinstance(e, HTTPException):
            return {'code': e.code, 'description': e.description}, e.code

        app.logger.exception(e)

        return {'code': InternalServerError.code,
                'description': InternalServerError.description}, InternalServerError.code

    @app.after_request
    def after_request(response):
        """Enable CORS."""
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Origin, X-Requested-With, Content-Type, Accept, Authorization')
        return response

    from .views import bp
    app.register_blueprint(bp)


def setup_wlts_managers():
    """Initialize the WLTS."""
    from .collections.collection_manager import collection_manager
    from .datasources.ds_manager import datasource_manager


__all__ = ('__version__', 'create_app', )
