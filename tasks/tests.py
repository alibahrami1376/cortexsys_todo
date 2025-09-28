from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Task  # فرض کردم مدل Task در این اپ وجود دارد

User = get_user_model()

class TaskAPITestCase(APITestCase):

    def test_task_list_requires_auth(self):
        url = reverse('task_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_authenticated(self):
        user = User.objects.create_user(username="u", email="u@example.com", password="pass1234")
        self.client.force_authenticate(user=user)

        url = reverse('task_list_create')
        data = {"title": "My Task", "priority": "high"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "My Task")
        self.assertEqual(response.data["priority"], "high")
        self.assertEqual(response.data["status"], "pending")

    def test_update_task_with_put(self):
        user = User.objects.create_user(username="u1", email="u1@example.com", password="pass1234")
        self.client.force_authenticate(user=user)

        task = Task.objects.create(title="Old Title", user=user, priority="low")

        url = reverse("task_detail", args=[task.id])
        data = {
            "title": "New Title",
            "description": "Updated via PUT",
            "priority": "high",
            "status": "completed",
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "New Title")
        self.assertEqual(task.status, "completed")
        self.assertEqual(task.priority, "high")

    def test_partial_update_task_with_patch(self):
        user = User.objects.create_user(username="u2", email="u2@example.com", password="pass1234")
        self.client.force_authenticate(user=user)

        task = Task.objects.create(title="Patch Me", user=user, priority="medium")

        url = reverse("task_detail", args=[task.id])
        data = {"priority": "low"}  # تغییر فقط priority
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.priority, "low")
        self.assertEqual(task.title, "Patch Me")
