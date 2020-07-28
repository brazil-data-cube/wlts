#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Utils for Web Land Trajectory Service."""

from pkg_resources import resource_string as load


def load_example_data(file):
    """Load data."""
    sql_dir = "example/{}".format(file)

    sql = load(__name__, sql_dir).decode()

    return sql

class CollectionsUtils:
    """CollectionsUtils Class."""

    @classmethod
    def describe(cls, collection):
        """Describe Collection."""
        try:
            data = {
                "name": collection.name,
                "description": collection.description,
                "detail": collection.detail,
                "collection_type": collection.get_collectiontype(),
                "resolution_unit": {
                    "unit": collection.get_resolution_unit(),
                    "value": collection.get_resolution_value()
                },
                "period": {
                    "start_date": collection.get_start_date(),
                    "end_date": collection.get_end_date()
                },
                "spatial_extent": collection.get_spatial_extent()
            }

            return data

        except:
            return None
