#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Feature Collection Class."""

from ..utils import get_date_from_str
from .collection import Collection


class FeatureCollection(Collection):
    """Implement a feature collection."""

    def __init__(self, collections_info):
        """Creates FeatureCollection.

        Args:
            collections_info (dict): The collection information.
        """
        super().__init__(collections_info["name"],
                         collections_info["authority_name"],
                         collections_info["description"],
                         collections_info["detail"],
                         collections_info["datasource_id"],
                         collections_info["dataset_type"],
                         collections_info["classification_class"],
                         collections_info["temporal"],
                         collections_info["scala"],
                         collections_info["spatial_extent"],
                         collections_info["period"])

        self.feature_name = collections_info["feature_name"]
        self.geom_property = collections_info["geom_property"]
        self.observations_properties = collections_info["observations_properties"]

    def collection_type(self):
        """Return collection type."""
        return "Feature"

    def trajectory(self, tj_attr, x, y, start_date, end_date, geometry):
        """Return the trajectory.

        Args:
            tj_attr (list): The list of trajectories.
            x (int/float): A longitude value according to EPSG:4326.
            y (int/float): A latitude value according to EPSG:4326.
            start_date (:obj:`str`, optional): The begin of a time interval.
            end_date (:obj:`str`, optional): The begin of a time interval.
            geometry (:obj:`str`, optional): Used to return geometry in trajectory.

         Returns:
            list: A trajectory object as a list.
        """
        ds = self.datasource

        for obs in self.observations_properties:

            args = {
                "feature_name": self.feature_name,
                "temporal": self.temporal,
                "x": x,
                "y": y,
                "obs": obs,
                "geom_property": self.geom_property,
                "start_date": start_date,
                "end_date": end_date,
                "classification_class": self.classification_class,
                "geometry_flag": geometry
            }

            result = ds.get_trajectory(**args)

            if result is not None:
                for i in result:
                    i["collection"] = self.get_name()
                    tj_attr.append(i)
