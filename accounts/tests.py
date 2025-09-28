from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationTestCase(APITestCase):

    def test_register_user(self):
        url = reverse('register')
        data = {
            "username": "tester",
            "email": "tester@example.com",
            "password": "pass1234"
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="tester@example.com").exists())
