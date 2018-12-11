import json

from rest_framework.test import APIClient
from django.test import TestCase
from rest_framework import status
from django.core import mail


class PasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.forgot_password = {'email': 'remmy@test.com'}

        self.reset_password = {
            'email': 'remmy@test.com',
            'token': '1234567890',
            'password': 'Password123'
        }

        self.renew_password = {
            'email': 'remmy@test.com',
            'old': 'password1',
            'new_password': 'Password123'
        }

        self.old_password = {'email': 'remmy@test.com', 'old': 'password1'}

    def test_send_forgot_password_mail(self):
        ''' Test that checks if a reset password mail is sent'''

        response = self.client.post(
            'api/users/forgot_password',
            data=json.dumps(self.forgot_password),
            format='json')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset link')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        ''' Test that checks if a user can reset password '''

        response = self.client.put(
            'api/users/forgot_password',
            data=json.dumps(self.reset_password),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.data)["message"],
            "Password updated successfully, you may now login")

    def test_renew_password(self):
        ''' Test that checks if a logged in user can renew password '''

        response = self.client.put(
            'api/users/forgot_password',
            data=json.dumps(self.renew_password),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.data)["message"],
            "Password updated successfully")

    def test_no_change_in_password(self):
        ''' Test that checks if the updated password is the \
        same as the new password '''

        self.client.post(
            'api/users/forgot_password',
            data=json.dumps(self.old_password),
            format='json')

        response = self.client.put(
            'api/users/forgot_password',
            data=json.dumps(self.renew_password),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.data)["message"],
            "New password cannot be the same as the old password")

            
