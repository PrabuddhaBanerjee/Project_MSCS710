# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.airline_results_airlines import AirlineResultsAirlines  # noqa: F401,E501
from swagger_server import util


class AirlineResults(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, airlines: List[AirlineResultsAirlines]=None):  # noqa: E501
        """AirlineResults - a model defined in Swagger

        :param airlines: The airlines of this AirlineResults.  # noqa: E501
        :type airlines: List[AirlineResultsAirlines]
        """
        self.swagger_types = {
            'airlines': List[AirlineResultsAirlines]
        }

        self.attribute_map = {
            'airlines': 'Airlines'
        }
        self._airlines = airlines

    @classmethod
    def from_dict(cls, dikt) -> 'AirlineResults':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The airlineResults of this AirlineResults.  # noqa: E501
        :rtype: AirlineResults
        """
        return util.deserialize_model(dikt, cls)

    @property
    def airlines(self) -> List[AirlineResultsAirlines]:
        """Gets the airlines of this AirlineResults.


        :return: The airlines of this AirlineResults.
        :rtype: List[AirlineResultsAirlines]
        """
        return self._airlines

    @airlines.setter
    def airlines(self, airlines: List[AirlineResultsAirlines]):
        """Sets the airlines of this AirlineResults.


        :param airlines: The airlines of this AirlineResults.
        :type airlines: List[AirlineResultsAirlines]
        """

        self._airlines = airlines
