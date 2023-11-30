#
# This file is part of WLTS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
#
"""This module WLTS Operations vocabularies."""
from json import loads as json_loads
from pathlib import Path

from wlts.config import BASE_DIR

schemas_folder = Path(BASE_DIR) / 'utils/jsonschemas/'


def load_schema(file_name):
    """Open file and parses as JSON file.

    :param file_name: File name of JSON Schema.
    """
    schema_file = schemas_folder / file_name

    with schema_file.open() as f:
        return json_loads(f.read())


root = load_schema('root.json')
collections_list = load_schema('list_collections_request.json')
collections_list_response = load_schema('list_collections_response.json')
describe_collection = load_schema('describe_collection_request.json')
describe_collection_response = load_schema('describe_collection_response.json')
trajectory = load_schema('trajectory_request.json')
trajectory_response = load_schema('trajectory_response.json')
