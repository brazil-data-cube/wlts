"""
Brazil Data Cube Configuration
You can define these configurations and call using environment variable
`ENVIRONMENT`. For example: `export ENVIRONMENT=ProductionConfig`
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def get_settings(env):
    """Retrieve Config class from environment"""
    return CONFIG.get(env)


class Config():
    """Base configuration with default flags"""
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "APi-Users-123456"


class ProductionConfig(Config):
    """Production Mode"""
    DEBUG = False


class DevelopmentConfig(Config):
    """Development Mode"""
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    """Testing Mode (Continous Integration)"""
    TESTING = True
    DEBUG = True


key = Config.SECRET_KEY

CONFIG = {
    "DevelopmentConfig": DevelopmentConfig(),
    "ProductionConfig": ProductionConfig(),
    "TestingConfig": TestingConfig()
}
