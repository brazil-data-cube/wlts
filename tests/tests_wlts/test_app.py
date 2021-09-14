#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Unit-test for WLTS' controller."""
import json
import pytest
import os
import re

from pkg_resources import resource_filename
from unittest.mock import patch

from wlts.utils.schemas import collections_list_response, \
    describe_collection_response, \
    trajectory_response, root
from jsonschema import validate

from wlts import create_app


@pytest.fixture(scope="session")
def mocks():
    mocks_dir = resource_filename(__name__, 'mocks/')
    mocks_files = os.listdir(mocks_dir)
    mocks = dict()
    for filename in mocks_files:
        if os.path.isfile(mocks_dir+filename):
            with open(mocks_dir+filename, 'r') as f:
                mocks[filename] = json.load(f)

    return mocks


@pytest.fixture
def requests_mock(requests_mock):
    requests_mock.get(re.compile('https://geojson.org/'), real_http=True)
    yield


@pytest.fixture(scope='class')
def mock_oauth2_cache():
    with patch('bdc_auth_client.decorators.token_cache') as mock:
        yield mock


@pytest.fixture(scope="class")
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


class TestWLTS:
    def _assert_json(self, response, expected_code: int = 200):
        assert response.status_code == expected_code
        assert response.content_type == 'application/json'

    def _configure_authentication_test(self, mock, roles):
        headers = {'x-api-key': 'SomeToken', 'Content-Type': 'application/json'}

        res = dict(sub=dict(roles=roles))

        mock.get.return_value(res)

        return headers

    def test_data_dir(self):
        assert os.path.join(os.path.dirname(__file__), '/json_configs/datasources.json')

    def test_root(self, client):
        response = client.get(f'/wlts/')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=root)

    def test_list_collection(self, client):
        response = client.get(f'/wlts/list_collections?access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=collections_list_response)

    def test_describe_collection_without_parameter(self, client):
        response = client.get(f'/wlts/describe_collection?access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=400)
        assert response.json['description'] == "\'collection_id\' is a required property"

    def test_describe_collection(self, client):
        response = client.get(f'/wlts/describe_collection?collection_id=deter_amz&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=describe_collection_response)

    def test_describe_collection_not_found(self, client):
        response = client.get(
            f'/wlts/describe_collection?collection_id=Invalid&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=404)
        assert response.json['description'] == "Collection Invalid not found!"

    def test_trajectory_without_lat(self, client):
        response = client.get(f'/wlts/trajectory?access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=400)
        assert response.json['description'] == "\'latitude\' is a required property"

    def test_trajectory_without_long(self, client):
        response = client.get(
            f'/wlts/trajectory?latitude=-12.662241&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=400)
        assert response.json['description'] == "\'longitude\' is a required property"

    def test_trajectory_without_collection(self, client):
        response = client.get(
            f'/wlts/trajectory?latitude=-9.091&longitude=-66.031&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=400)
        assert response.json['description'] == "\'collections\' is a required property"

    def test_trajectory(self, client):
        response = client.get(
            f'/wlts/trajectory?collections=deter_amz&latitude=-9.091&longitude=-66.031&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=trajectory_response)

    def test_trajectory_start_date(self, client):
        response = client.get(
            f'/wlts/trajectory?collections=deter_amz&latitude=-9.091&longitude=-66.031&start_date=2016-10-07'
            f'&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=trajectory_response)

    def test_trajectory_end_date(self, client):
        response = client.get(
            f'/wlts/trajectory?collections=deter_amz&latitude=-9.091&longitude=-66.031&end_date=2020-07-15'
            f'&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=trajectory_response)

    def test_trajectory_geometry(self, client):
        response = client.get(
            f'/wlts/trajectory?collections=deter_amz&latitude=-9.091&longitude=-66.031&geometry=True'
            f'&access_token={os.getenv("WLTS_TEST_ACCESS_TOKEN")}')

        self._assert_json(response, expected_code=200)
        validate(instance=response.json, schema=trajectory_response)
