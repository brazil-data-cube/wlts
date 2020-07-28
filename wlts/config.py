#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Brazil Data Cube Configuration."""
import os

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
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'postgresql://postgres:postgres@localhost:5432/wlts')
    WLTS_URL = os.getenv('WLTS_URL', 'http://localhost:5000')


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
