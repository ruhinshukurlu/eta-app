"""
Tests for the API views placed in the todo/api/views.py
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

REGISTER_URL = reverse("todo:register")
LOGIN_URL = reverse("todo:login")
CREATE_EXPECTATION_URL = reverse("todo:create-expectation")
EXPECTATION_LIST_URL = reverse("todo:active-expectations")


class UserRegisterViewTests(APITestCase):
    """Tests for the user registration view"""

    def test_user_registration(self):
        """Test user register"""

        url = REGISTER_URL
        data = {"username": "usertest", "email": "user@example.com", "password": "testpass123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "usertest")
        self.assertEqual(response.data["email"], "user@example.com")
        self.assertFalse("password" in response.data)

    def test_user_registr_with_existing_username(self):

        url = REGISTER_URL
        data = {"username": "usertest", "email": "user@example.com", "password": "testpass123"}
        User.objects.create_user(**data)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(APITestCase):
    """Tests for the user login view"""

    def setUp(self):
        self.user = User.objects.create_user(username="usertest", email="user@example.com", password="testpass123")
        self.login_url = LOGIN_URL

    def test_user_login(self):
        """Test user login success"""
        data = {"username": "usertest", "password": "testpass123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)

    def test_user_login_with_invalid_credentials(self):
        """Test user login with invalid credentials"""
        data = {"username": "usertest", "password": "testpass1234"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateExpectationViewTests(APITestCase):
    """Tests for the create expectation view"""

    def setUp(self):
        self.user = User.objects.create_user(username="usertest", email="user@example.com", password="testpass123")
        self.client.force_authenticate(self.user)  # we need to login the created test user
        self.cerate_expectation_url = CREATE_EXPECTATION_URL

    def test_create_expectation(self):
        """Test creating expectation successfully"""
        data = {"project_name": "foo", "issue": "2", "expected_at": "2023-08-07T08:59:51.977Z"}
        response = self.client.post(self.cerate_expectation_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_expected_date_with_invalid_value(self):
        data = {
            "project_name": "foo",
            "issue": "2",
            "expected_at": "2023-06-07T08:59:51.977Z",  # expected date is less that current time
        }
        response = self.client.post(self.cerate_expectation_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_two_active_eta(self):
        # creating first eta
        data1 = {"project_name": "foo", "issue": "2", "expected_at": "2023-08-07T08:59:51.977Z"}
        self.client.post(self.cerate_expectation_url, data1)

        # trying to create second active eta
        data2 = {"project_name": "foo 2", "issue": "3", "expected_at": "2023-08-07T08:59:51.977Z"}
        response = self.client.post(self.cerate_expectation_url, data2)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ExpectationListViewTests(APITestCase):
    def test_expectation_list(self):
        """Test expectation list view"""
        url = EXPECTATION_LIST_URL
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
