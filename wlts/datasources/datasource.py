#
# This file is part of WLTS.
# Copyright (C) 2022 INPE.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.html>.
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
