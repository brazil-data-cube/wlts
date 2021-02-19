#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Brazil Data Cube Configuration."""
import os

from packaging import version as _version

from .version import __version__

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_settings(env):
    """Retrieve Config class from environment."""
    return CONFIG.get(env)


class Config():
    """Base configuration with default flags."""

    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "APi-Users-123456"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WLTS_URL = os.getenv('WLTS_URL', 'http://localhost:5000')

    WLTS_API_VERSION = _version.parse(__version__).base_version


class ProductionConfig(Config):
    """Production Mode."""

    DEBUG = False


class DevelopmentConfig(Config):
    """Development Mode."""

    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)."""

    TESTING = True
    DEBUG = True


key = Config.SECRET_KEY

CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}
