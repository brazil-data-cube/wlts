#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""This module WLTS Operations vocabularies."""
from json import loads as json_loads
from pathlib import Path

from wlts.config import BASE_DIR

schemas_folder = Path(BASE_DIR) / 'jsonschemas/'


def load_schema(file_name):
    """Open file and parses as JSON file.

    :param file_name: File name of JSON Schema.
    """
    schema_file = schemas_folder / file_name

    with schema_file.open() as f:
        return json_loads(f.read())


collections_list = load_schema('list_collections_request.json')
collections_list_response = load_schema('list_collections_response.json')
describe_collection = load_schema('describe_collection_request.json')
describe_collection_response = load_schema('describe_collection_response.json')
trajectory = load_schema('trajectory_request.json')
trajectory_response = load_schema('trajectory_response.json')