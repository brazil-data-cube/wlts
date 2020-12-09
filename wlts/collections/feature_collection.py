#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2019-2020 INPE.
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

    def trajectory(self, tj_attr, x, y, start_date, end_date):
        """Return the trajectory.

        Args:
            tj_attr (list): The list of trajectories.
            x (int/float): A longitude value according to EPSG:4326.
            y (int/float): A latitude value according to EPSG:4326.
            start_date (:obj:`str`, optional): The begin of a time interval.
            end_date (:obj:`str`, optional): The begin of a time interval.

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
                "end_date": end_date
            }

            result = ds.get_trajectory(**args)

            obs_info = None

            if result is not None:

                # Get Class information by passing trajectory result
                if self.temporal["type"] == "STRING":
                    obs_info = get_date_from_str(obs["temporal_property"])
                    obs_info = obs_info.strftime(self.temporal["string_format"])

                elif self.temporal["type"] == "DATE":
                    obs_info = result[obs["temporal_property"]]

                # Get Class
                if self.classification_class.get_type() == "Literal":
                    class_info = obs["class_property_name"]

                elif self.classification_class.get_type() == "Self":
                    class_info = result[obs["class_property"]]
                else:
                    feature_id = result[obs["class_property"]]

                    ds_class = self.classification_class.get_class_ds()

                    if self.classification_class.get_type() == 'Self':
                        class_info = ds_class.get_classe(feature_id,
                                                         self.classification_class.get_class_property_value(),
                                                         self.classification_class.get_class_property_name(),
                                                         self.classification_class.get_classification_system_name())
                    else:
                        class_info = ds_class.get_classe(feature_id,
                                                         self.classification_class.get_class_property_value(),
                                                         self.classification_class.get_class_property_name(),
                                                         self.classification_class.get_property_name(),
                                                         class_system=self.get_classification_system_name)

                trj = {
                    "collection": self.get_name(),
                    "class": class_info,
                    "date": str(obs_info)
                }

                tj_attr.append(trj)

