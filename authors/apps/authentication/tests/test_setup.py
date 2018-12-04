from rest_framework.test import APIClient
from django.test import TestCase


class BaseSetUp(TestCase):
    """Base class for all the test classes"""

    def setUp(self):
        """Initialize test data"""
        self.client = APIClient()
        self.reg_data = {
            'username': 'remmy',
            'email': 'remmy@test.com',
            'password': 'Password123'
        }
        self.login_data = {
            'username': self.reg_data['username'],
            'password': self.reg_data['password']
        }
        # register a user
        self.client.post(
            'api/users',
            self.reg_data,
            format="json")
        # login the user
        self.login_res = self.client.post(
            'api/users/login',
            self.login_data,
            format="json")
        self.token = self.login_res.data['Token']
