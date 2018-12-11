import json
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .test_setup import BaseSetUp


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.base = BaseSetUp()

        self.login_data = {
            "username": "remmy",
            "password": "hgfhdbfsjhb"
        }

    def test_register_user_successfully(self):
        """Test that checks if a user instance is created."""

        response = self.client.post(
            "api/users",
            data=json.dumps(self.base.reg_data),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response[
                         "message"], "User created successfully")

    def test_empty_username_field(self):
        """Test that checks if the username input is empty."""
        self.empty_username = {
            "username": "",
            "email": "remmy@test.com",
            "password": "Password123"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.empty_username),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Username field cannot be left empty")

    def test_empty_email_field(self):
        """Test that checks if the email input is empty."""
        self.empty_email = {
            "username": "remmy",
            "email": "",
            "password": "Password123"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.empty_email),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Email field cannot be left empty")

    def test_empty_password_field(self):
        """Test that checks if the password input is empty."""
        self.empty_password = {
            "username": "remmy",
            "email": "remmy@test.com",
            "password": ""
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.empty_password),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Password field cannot be left empty")

    def test_valid_username(self):
        """Test that checks if the username has valid input."""
        self.valid_username = {
            "username": "1@1#%^()+",
            "email": "remmytestcom",
            "password": "Password123"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.valid_username),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Valid username should be greater than 4 \
                            characters, may contain alphanumeric, '_', '@',\
                            '+', '.' and '-' characters")

    def test_valid_email(self):
        """Test that checks if the email has valid input."""
        self.valid_email = {
            "username": "remmy",
            "email": "remmytestcom",
            "password": "Password123"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.valid_email),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Valid email should be alphanumeric with \
                         the @ and . symbol")

    def test_invalid_password(self):
        """Test that checks if the password has valid input."""
        self.valid_password = {
            "username": "remmyk",
            "email": "remmyk@testcom",
            "password": "1234567890"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.valid_password),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Valid password should be more than 8 \
                         characters, alphanumeric, have at least one capital \
                         letter and a symbol")

    def test_duplicate_username(self):
        """Test that checks if the username already exists."""
        self.duplicate_username = {
            "username": "remmy",
            "email": "remmy@testcom",
            "password": "Password123"
        }

        self.duplicate_username2 = {
            "username": "remmy",
            "email": "remmyk@testcom",
            "password": "Password123"
        }

        self.client.post(
            "api/users",
            data=json.dumps(self.duplicate_username),
            format="json")

        response = self.client.post(
            "api/users",
            data=json.dumps(self.duplicate_username2),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Username already exists")

    def test_duplicate_email(self):
        """Test that checks if the email already exists."""
        self.duplicate_email = {
            "username": "remmy",
            "email": "remmyk@testcom",
            "password": "Password123"
        }

        self.duplicate_email2 = {
            "username": "remmyk",
            "email": "remmyk@testcom",
            "password": "Password123"
        }

        self.client.post(
            "api/users",
            data=json.dumps(self.duplicate_email),
            format="json")
        response = self.client.post(
            "api/users/register",
            data=json.dumps(self.duplicate_email2),
            format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Email already exists")

    def test_missing_data(self):
        """Test that checks if the required fields exists."""

        response = self.client.post(
            "api/users",
            data=json.dumps({}),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Username, email and password are \
                         required fields")

    def test_missing_username(self):
        """Test that checks if the required username field exists."""
        self.missing_username = {
            "email": "remmyk@testcom",
            "password": "Password123"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.missing_username),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Username is a required field")

    def test_missing_email(self):
        """Test that checks if the required email field exists."""
        self.missing_email = {
            "username": "remmy",
            "password": "Password123"
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.missing_email),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Email is a required field")

    def test_missing_password(self):
        """ Test that checks if the required password field exists."""
        self.missing_password = {
            "username": "remmyk",
            "email": "remmyk@testcom",
        }

        response = self.client.post(
            "api/users",
            data=json.dumps(self.missing_password),
            format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.data)[
                         "message"], "Password is a required field")
