#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Command Line Interface Web Land Trajectory Service."""

import click
from flask.cli import FlaskGroup, with_appcontext

from . import create_app
from .ext import db as _db
from .utils import load_exemple_data


def create_cli(create_app=None):
    """Define a Wrapper creation of Flask App in order to attach into flask click.

    Args:
         create_app (function) - Create app factory (Flask)
    """
    def create_cli_app(info):
        """Describe flask factory to create click command."""
        if create_app is None:
            info.create_app = None

            app = info.load_app()
        else:
            app = create_app()

        return app

    @click.group(cls=FlaskGroup, create_app=create_cli_app)
    def cli(**params):
        """Command line interface for wlts."""
        pass

    return cli


cli = create_cli(create_app=create_app)


@cli.group()
@with_appcontext
def db():
    """Database operations."""


@db.command()
@with_appcontext
def insert_db():
    """Insert Exemple Data into Database."""
    sql = load_exemple_data('wlts_example.sql')

    _db.session.execute(sql)

    _db.session.commit()

    click.echo("Schema Create!")