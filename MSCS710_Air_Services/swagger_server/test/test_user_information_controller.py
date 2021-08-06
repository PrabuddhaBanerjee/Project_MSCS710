# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.test import BaseTestCase


class TestUserInformationController(BaseTestCase):
    """UserInformationController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user
        Create user
        """
        body = {
  "email" : "email@email.com",
  "username" : "username1",
  "password" : "password1"
}
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/register',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login_user(self):
        """Test case for login_user
        Login user
        """
        body = {
  "email" : "email@email.com",
  "password" : "password1"
}
        response = self.client.open(
            '/csumano/AIRservices/1.0.0/login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()