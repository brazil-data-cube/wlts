#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Web Land Trajectory Service."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class WLTSDatabase:
    """WLTS Database."""

    def __init__(self, app=None, **kwargs):
        """WLTS Database init."""
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app: Flask, **kwargs):
        """WLTS Database init app."""
        db.init_app(app)

        app.extensions['wlts'] = self
