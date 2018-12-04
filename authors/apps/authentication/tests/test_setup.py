from rest_framework.test import APIClient
from django.test import TestCase


class BaseSetUp(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_user = {
            'username': 'remmy',
            'email': 'remmy@test.com',
            'password': 'Password123'
        }
        self.token = 'ou9ru32r9uror0ur29ur2yr927r923ry93u'
