from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Task

# Create your tests here.
class AuthTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )

    def test_login_user(self):
        url = reverse("token_obtain_pair")  # si tu utilises JWT
        response = self.client.post(url, {"email": "test@example.com", "password": "testpass123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)  # vérifie qu'on a un token


class TaskTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.client.force_authenticate(user=self.user)  # connecte l’utilisateur
        self.task_url = reverse("task-list")  # correspond à ton endpoint DRF

    def test_create_task(self):
        data = {"title": "Nouvelle tâche", "description": "Ceci est un test"}
        response = self.client.post(self.task_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "Nouvelle tâche")

    def test_list_tasks(self):
        Task.objects.create(title="Tâche 1", description="Test", user=self.user)
        Task.objects.create(title="Tâche 2", description="Encore un test", user=self.user)

        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 2)  # si pagination activée

    def test_update_task(self):
        task = Task.objects.create(title="Ancien titre", description="Test", user=self.user)
        url = reverse("task-detail", args=[task.id])

        response = self.client.patch(url, {"title": "Nouveau titre"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, "Nouveau titre")

    def test_delete_task(self):
        task = Task.objects.create(title="À supprimer", description="Test", user=self.user)
        url = reverse("task-detail", args=[task.id])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)
