#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS Image Collection Class."""
from .collection import Collection


class ImageCollection(Collection):
    """Implement a image collection."""

    def __init__(self, collections_info):
        """Creates ImageCollection.

        Args:
            collections_info (dict): The collection information.
        """
        super().__init__(collections_info["name"],
                         collections_info["title"],
                         collections_info["authority_name"],
                         collections_info["description"],
                         collections_info["detail"],
                         collections_info["datasource_id"],
                         collections_info["dataset_type"],
                         collections_info["classification_class"],
                         collections_info["temporal"],
                         collections_info["scala"],
                         collections_info["spatial_extent"],
                         collections_info["period"],
                         collections_info["is_public"],
                         collections_info["deprecated"])

        self.grid = collections_info["grid"]
        self.spatial_ref_system = collections_info["spatial_reference_system"]
        self.observations_properties = collections_info["attributes_properties"]
        self.timeline = collections_info["timeline"]

        self.validade_collection()

    def validade_collection(self) -> None:
        """Verify if collection exist in datasource."""
        ds = self.get_datasource()

        for att in self.observations_properties:
            ds.check_image(workspace=att["workspace"], ft_name=att["image"])

        return

    def collection_type(self):
        """Return the collection type."""
        return "Image"

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
        ds = self.get_datasource()

        for time in self.timeline:
            for att in self.observations_properties:
                args = {
                    "image": att["image"],
                    "temporal": self.temporal,
                    "workspace": att["workspace"],
                    "x": x,
                    "y": y,
                    "grid": self.grid,
                    "srid": self.spatial_ref_system["srid"],
                    "start_date": start_date,
                    "end_date": end_date,
                    "time": time,
                    "classification_class": self.classification_class,
                    "geometry_flag": geometry
                }

                result = ds.get_trajectory(**args)

                if result is not None:
                    result["collection"] = self.get_name()
                    tj_attr.append(result)

