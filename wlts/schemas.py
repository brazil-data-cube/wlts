"""
This module WLTS Operations vocabularies.
It is defined as `request` and `response` objects.
Attributes:
    collections_list (dict): JSON Schema of WLTS ListCollections request
    describe_collections (dict): JSON Schema of WLTS DescribeCollection request
    trajectory (dict): JSON Schema of WLTS Trajectory request


"""

from json import loads as json_loads
from pathlib import Path

from wlts.config import BASE_DIR

schemas_folder = Path(BASE_DIR) / 'json-schemas/'


def load_schema(file_name):
    """
    Open file and parses as JSON file
    Args:
        file_name (str): File name of JSON Schema
    Returns:
        JSON schema parsed as Python object (dict)
    Raises:
        json.JSONDecodeError When file is not valid JSON object
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
list_classification_system = load_schema('list_classification_sytem_request.json')
