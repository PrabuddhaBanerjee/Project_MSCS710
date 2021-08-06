# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.body2 import Body2  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAirlineInformationController(BaseTestCase):
    """AirlineInformationController integration test stubs"""

    def test_best_airlines(self):
        """Test case for best_airlines

        Best airports
        """
        body = Body()
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/bestairlines',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_flight_predictor(self):
        """Test case for flight_predictor

        Flight predictor
        """
        body = Body2()
        query_string = [('model', 'model_example')]
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/flightpredictor',
            method='POST',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_gather_flights(self):
        """Test case for gather_flights

        Gather flight data
        """
        query_string = [('year', 56),
                        ('month', 56),
                        ('day', 56),
                        ('origin', 'origin_example'),
                        ('destination', 'destination_example')]
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/flights',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()