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


__all__ = ('__version__', 'create_app')
