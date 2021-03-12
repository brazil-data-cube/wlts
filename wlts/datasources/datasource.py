#
# This file is part of Web Land Trajectory Service.
# Copyright (C) 2020-2021 INPE.
#
# Web Land Trajectory Service is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""WLTS DataSource Abstract Collection."""
from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):
    """Abstract class to represent an Data Source."""

    def __init__(self, id):
        """Abstraction to make DataSource.

        Args:
            id (str): Identifier of an datasource.
        """
        self._id = id

    @property
    def get_id(self):
        """Return the datasource identifier (id)."""
        return self._id

    @abstractmethod
    def get_type(self):
        """Return the datasource type."""
        pass
