import json

from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.core import mail
from .test_setup import BaseSetUp


class PasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base = BaseSetUp()

        self.login_data = {
            "username": self.base.reg_data['username'],
            "password": self.base.reg_data['password']
        }
        # login the user
        self.login_res = self.client.post(
            "api/users/login",
            self.login_data,
            format="json")
        self.token = self.login_res.data['Token']
        self.base.client.credentials(HTTP_AUTHORIZATION='Token' + self.token)

    def test_send_forgot_password_mail(self):
        """Test that checks if a reset password mail is sent"""
        self.forgot_password = {
            "email": "remmy@test.com",
        }

        self.login_res = self.client.post(
            "api/users/login", self.login_data, format="json")
        response = self.client.post("api/users/forgot_password",
                                    data=json.dumps(self.forgot_password),
                                    format="json")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Password reset link")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reset_password(self):
        """Test that checks if a user who forgot their password can reset it"""
        self.base.client.credentials()
        self.reset_password = {
            "email": "remmy@test.com",
            "new_password": "Password123"
        }

        response = self.client.put("api/users/response_password",
                                   data=json.dumps(self.reset_password),
                                   format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data)["message"],
                         "Password updated successfully")

    def test_renew_password(self):
        """Test that checks if a logged in user can change their password"""
        self.renew_password = {
            "email": "remmy@test.com",
            "old_password": "password1",
            "new_password": "Password123"
        }

        response = self.client.put(
            'api/users/renew_password',
            data=json.dumps(self.renew_password),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.data)["message"],
                         "Password updated successfully")

    def test_no_change_in_password(self):
        """Test that checks if the updated password is the \
            same as the new password"""
        self.reset_password = {
            "email": "remmy@test.com",
            "old": "password123",
            "new_password": "Password123"
        }

        response = self.client.put(
            "api/users/reset_password",
            data=json.dumps(self.reset_password),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(json.loads(response.data)["message"],
                         "New password cannot be the same as the old \
                            password")
