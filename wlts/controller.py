#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Controllers of Web Land Trajectory Service."""
from flask import abort

from wlts.collections.collection_manager import collection_manager


def describe_collection(collection_name, roles=[]):
    """Describe Collection."""
    collection = collection_manager.get_collection(collection_name)

    if collection is None:
        abort(404, "Collection Not Found")

    if eval(collection.is_public) is False and collection_name not in roles:
        abort(403, "Forbidden")

    try:
        classification_system = collection.classification_class

        describe = dict()

        describe["classification_system"] = {
            "type": classification_system.get_type(),
            "classification_system_name": classification_system.get_classification_system_name(),
            "classification_system_id": classification_system.get_classification_system_id(),
            "classification_system_version": classification_system.get_classification_system_version()
        }

        describe["name"] = collection.name
        describe["description"] = collection.description
        describe["detail"] = collection.detail
        describe["collection_type"] = collection.collection_type()
        describe["resolution_unit"] = {
            "unit": collection.get_resolution_unit(),
            "value": float(collection.get_resolution_value())
        }
        describe["period"] = {
            "start_date": collection.get_start_date(),
            "end_date": collection.get_end_date()
        }
        describe["spatial_extent"] = collection.get_spatial_extent()

        return describe

    except Exception:
        abort(403, "Error while retrieve collection metadata")
