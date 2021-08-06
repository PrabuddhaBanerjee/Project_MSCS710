# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.body1 import Body1  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAirlineAndWeatherInformationController(BaseTestCase):
    """AirlineAndWeatherInformationController integration test stubs"""

    def test_flight_graphs(self):
        """Test case for flight_graphs

        Gather graphs
        """
        query_string = [('graph', 'graph_example'),
                        ('year', 'year_example')]
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/flightgraphs',
            method='POST',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_weather_airline(self):
        """Test case for weather_airline

        Weather comapred to flights
        """
        body = Body1()
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/weathertoflights',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()