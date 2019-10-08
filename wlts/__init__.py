import os
from wlts.config import get_settings
from wlts.blueprint import blueprint
from flask import Flask
from flask_cors import CORS

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
