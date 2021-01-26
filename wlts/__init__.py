#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
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


def create_app(config_name):
    """Creates Brazil Data Cube WLTS application from config object.

    :param config_name: Config instance.
    :type config_name:string|wlts.config.Config

    :returns: Flask Application with config instance scope.
    """
    app = Flask(__name__)

    conf = config.get_settings(config_name)

    app.config.from_object(conf)

    setup_app(app)

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

    from .views import bp

    app.register_blueprint(bp)


app = create_app(os.environ.get('WLTS_ENVIRONMENT', 'DevelopmentConfig'))

__all__ = ('__version__', 'create_app')
