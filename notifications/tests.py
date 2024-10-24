from django.test import TestCase
from django.urls import reverse
from .models import Notifications


class NotificationsInboxTest(TestCase):
    def setUp(self):
        self.url = reverse("notifications:inbox")

    def test_inbox_view_get(
        self,
    ):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "notifications/inbox.html")


class GetNotificationsTest(TestCase):
    def setUp(self):
        Notifications.objects.create(content="Test Notification 1")
        Notifications.objects.create(content="Test Notification 2")
        Notifications.objects.create(content="Test Notification 3", active=False)
        self.url = reverse("notifications:get_notifications")

    def test_get_notifications(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()["notifications"]
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["content"], "Test Notification 2")
        self.assertEqual(data[1]["content"], "Test Notification 1")
