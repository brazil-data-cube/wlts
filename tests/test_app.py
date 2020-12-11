#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Unit-test for WLTS' controller."""
import pytest

from wlts.schemas import collections_list_response, \
    describe_collection_response, \
    trajectory_response
from json import loads as json_loads
from jsonschema import validate

from wlts import create_app


@pytest.fixture(scope="class")
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


class TestWLTS:
    def list_collection(self, client):
        response = client.get('/wlts/list_collections')

        assert response.status_code == 200

        collection_response = json_loads(self.response.data.decode('utf-8'))

        validate(instance=collection_response, schema=collections_list_response)

    def describe_collection_without_parameter(self, client):
        response = client.get('/wlts/describe_collection')

        response_json = json_loads(response.data.decode('utf-8'))

        assert response.status_code == 400
        assert response_json['message'] == "\'collection_id\' is a required property"

    def describe_collection(self, client):
        response = client.get(
            '/wlts/describe_collection?collection_id={}'.format("deter_amz")
        )

        collection_response = json_loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert response.conten_type == "application/json"
        validate(instance=collection_response, schema=describe_collection_response)

    def describe_collection_not_found(self, client):
        response = client.get(
            '/wlts/describe_collection?collection_id={}'.format("Prodes")
        )

        collection_response = json_loads(response.data.decode('utf-8'))

        assert response.status_code == 404
        assert collection_response['message'] == "Collection Not Found"

    def trajectory_without_lat(self, client):

        response = client.get('/wlts/trajectory')

        collection_response = json_loads(response.data.decode('utf-8'))

        assert response.status_code == 400
        assert collection_response['message'] == "\'latitude\' is a required property"

    def trajectory_without_long(self, client):

        response = client.get('/wlts/trajectoy?latitude=-12.662241')

        collection_response = json_loads(response.data.decode('utf-8'))

        assert response.status_code == 400
        assert collection_response['message'] == "\'longitude\' is a required property"

    def trajectory(self, client):

        response = client.get('/wlts/trajectoy?latitude=-9.091&longitude=-66.031')

        response_json = json_loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert response.conten_type == "application/json"
        validate(instance=response_json, schema=trajectory_response)
