#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for WLTS' controller."""

import  pytest
import unittest
from wlts import app as wlts_app
from wlts.schemas import collections_list_response, describe_collection_response, trajectory_response

from json import loads as json_loads
from jsonschema import validate

@pytest.fixture
def app():

    app = wlts_app.test_client()

    return app

def test_get_list_collections(app):

    response = app.get('/wlts/list_collections')

    assert 200 == response.status_code

def  test_list_collections_response(app):

    response = app.get('/wlts/list_collections')

    assert response.content_type == 'application/json'


#
# def test_list_collections():
#
#
#
#     assertEqual(200, self.response.status_code)
#
#
#     assert 1 == 1
