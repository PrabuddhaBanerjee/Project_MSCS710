# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Body1(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, year: int=None, month: int=None, day: int=None, city: str=None):  # noqa: E501
        """Body1 - a model defined in Swagger

        :param year: The year of this Body1.  # noqa: E501
        :type year: int
        :param month: The month of this Body1.  # noqa: E501
        :type month: int
        :param day: The day of this Body1.  # noqa: E501
        :type day: int
        :param city: The city of this Body1.  # noqa: E501
        :type city: str
        """
        self.swagger_types = {
            'year': int,
            'month': int,
            'day': int,
            'city': str
        }

        self.attribute_map = {
            'year': 'year',
            'month': 'month',
            'day': 'day',
            'city': 'city'
        }
        self._year = year
        self._month = month
        self._day = day
        self._city = city

    @classmethod
    def from_dict(cls, dikt) -> 'Body1':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The body_1 of this Body1.  # noqa: E501
        :rtype: Body1
        """
        return util.deserialize_model(dikt, cls)

    @property
    def year(self) -> int:
        """Gets the year of this Body1.


        :return: The year of this Body1.
        :rtype: int
        """
        return self._year

    @year.setter
    def year(self, year: int):
        """Sets the year of this Body1.


        :param year: The year of this Body1.
        :type year: int
        """

        self._year = year

    @property
    def month(self) -> int:
        """Gets the month of this Body1.


        :return: The month of this Body1.
        :rtype: int
        """
        return self._month

    @month.setter
    def month(self, month: int):
        """Sets the month of this Body1.


        :param month: The month of this Body1.
        :type month: int
        """

        self._month = month

    @property
    def day(self) -> int:
        """Gets the day of this Body1.


        :return: The day of this Body1.
        :rtype: int
        """
        return self._day

    @day.setter
    def day(self, day: int):
        """Sets the day of this Body1.


        :param day: The day of this Body1.
        :type day: int
        """

        self._day = day

    @property
    def city(self) -> str:
        """Gets the city of this Body1.


        :return: The city of this Body1.
        :rtype: str
        """
        return self._city

    @city.setter
    def city(self, city: str):
        """Sets the city of this Body1.


        :param city: The city of this Body1.
        :type city: str
        """

        self._city = city
