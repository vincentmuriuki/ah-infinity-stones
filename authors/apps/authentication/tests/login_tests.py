"""This module runs tests for user login process"""
import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class UserTestCase(TestCase):
    """This class contains tests for the user login process wihtout social authentication"""
    def setUp(self):
        """This function defines variables tobe used within the class"""
        self.client = APIClient()
        self.test_user = {'email' : 'remmy@test.com',
                          'password' : 'Password123'}
        self.test_unknown_user = {'email' : 'john@doe.com',
                                  'password' : 'Password123'}
        self.test_password = {'email' : 'remmy@test.com',
                              'password' : 'passssssss'}
    def test_login_user(self):
        """This function tests whether a registered user can login"""
        response = self.client.post(
            'api/users/login',
            data=json.dumps(self.test_user),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data)["message"],
                         "User logged in successfully")
        self.assertNotEqual(json.loads(response.data)["token"], None)
    def test_cannot_login_unregistered_user(self):
        """This function tests whether an unregistered user can login"""
        response = self.client.post(
            'api/users/login',
            data=json.dumps(self.test_unknown_user),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"], "User does not exist.")
        self.assertEqual(json.loads(response.data)["token"], None)
    def test_cannot_login_user_with_wrong_password(self):
        """This function tests whether a registered user can login with wrong password"""
        response = self.client.post(
            'api/users/login',
            data=json.dumps(self.test_password),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(json.loads(response.data)["message"],
                         "Either the email and/or the password is wrong.")
        self.assertEqual(json.loads(response.data)["token"], None)
        