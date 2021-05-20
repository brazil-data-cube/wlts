#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""This file contains the common validators used through Brazil Data Cube projects."""

from functools import wraps

from flask import request
from jsonschema import (SchemaError, ValidationError, draft7_format_checker,
                        validate)
from werkzeug.exceptions import BadRequest


def require_model(schema, draft=draft7_format_checker):
    """Require a JSON schema object to validate request query arguments.

    You can use it with APIResource in order to format BadRequestError output.

    TODO: Improve decorator to support request POST data values

    Args:
        schema (dict): JSON schema with Python Dictionaries.
        draft (jsonschema.FormatChecker, optional): JSON Schema format.

    Raises:
        BadRequest: When request arguments do not match with JSON schema.
    """
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            try:
                validate(instance=request.args,
                         schema=schema,
                         format_checker=draft)
            except (SchemaError, ValidationError) as e:
                raise BadRequest(e.message)
            return fn(*args, **kwargs)
        return decorated_function
    return decorator