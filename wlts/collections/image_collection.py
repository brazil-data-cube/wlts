#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Image Collection Class."""
from ..utils import get_date_from_str
from .collection import Collection


class ImageCollection(Collection):
    """Implement a image collection."""

    def __init__(self, collections_info):
        """Creates ImageCollection.

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

        self.image = collections_info["image"]
        self.grid = collections_info["grid"]
        self.spatial_ref_system = collections_info["spatial_reference_system"]
        self.observations_properties = collections_info["attributes_properties"]
        self.timeline = collections_info["timeline"]

    def collection_type(self):
        """Return the collection type."""
        return "Image"

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
        ds = self.get_datasource()

        for obs in self.observations_properties:
            for time in self.timeline:
                args = {
                    "image": self.image,
                    "temporal": self.temporal,
                    "x": x,
                    "y": y,
                    "grid": self.grid,
                    "srid": self.spatial_ref_system["srid"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "time": time
                }

                result = ds.get_trajectory(**args)

                obs_info = None
                class_info = None

                if result is not None:

                    # Get Class information by passing trajectory result
                    obs_info = get_date_from_str(time)
                    obs_info = obs_info.strftime(self.temporal["string_format"])

                    # Get Class
                    if self.classification_class.get_type() == "Literal":
                        class_info = obs["class_property_name"]

                    elif self.classification_class.get_type() == "Self":
                        class_info = result['raster_value']

                    else:

                        ds_class = self.classification_class.get_class_ds()

                        class_info = ds_class.get_classe(result['raster_value'],
                                                         self.classification_class.get_class_property_value(),
                                                         self.classification_class.get_class_property_name(),
                                                         self.classification_class.get_property_name(),
                                                         class_system=self.classification_class
                                                         .get_classification_system_name())

                    trj = {
                        "collection": self.get_name(),
                        "class": class_info,
                        "date": str(obs_info)
                    }

                    tj_attr.append(trj)
