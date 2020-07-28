#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Controllers of Web Land Trajectory Service."""

from wlts.collections.collection_manager import collection_manager


def describe_collection(collection_name):
    """Describe Collection."""
    collection = collection_manager.get_collection(collection_name)

    if collection is None:
        return collection
    try:
        data = {
            "name": collection.name,
            "description": collection.description,
            "detail": collection.detail,
            "collection_type": collection.collection_type(),
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

    # TODO melhorar o retorno dos erros
    except:
        return None
