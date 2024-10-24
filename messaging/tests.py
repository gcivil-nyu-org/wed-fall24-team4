from django.test import TestCase, Client
from django.urls import reverse
from .models import Message
from django.contrib.auth.models import User


class MessagingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword@1234"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword@1234"
        )
        self.user3 = User.objects.create_user(
            username="testuser3", password="testpassword@1234"
        )

        self.message1 = Message.objects.create(
            sender=self.user, recipient=self.user2, content="message 1"
        )
        self.message2 = Message.objects.create(
            sender=self.user2, recipient=self.user, content="message 2"
        )

    def test_inbox_view_get(self):
        self.client.force_login(self.user)
        url = reverse("messaging:inbox")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messaging/inbox.html")

    def test_inbox_search(self):
        self.client.force_login(self.user)
        url = reverse("messaging:inbox")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["conversation_history"][self.user2.username]["content"],
            "message 2",
        )
        self.assertEqual(response.context["start_conversations"], [])

        form_data = {"query": "testuser3"}
        response = self.client.get(url, data=form_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.context["conversation_history"]), 0)
        self.assertEqual(response.context["start_conversations"], [self.user3.username])

        form_data = {"query": "testuser"}
        response = self.client.get(url, data=form_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            response.context["conversation_history"][self.user2.username]["content"],
            "message 2",
        )
        self.assertEqual(response.context["start_conversations"], [self.user3.username])

    def test_direct_messaging_view(self):
        self.client.force_login(self.user)
        url = reverse("messaging:direct_messaging", args=[self.user2.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "messaging/direct_messaging.html")

        self.assertEqual(len(response.context["messages"]), 2)
        self.assertEqual(response.context["messaging_partner"], self.user2.username)

    def test_get_new_messages(self):
        self.client.force_login(self.user)
        url = reverse("messaging:get_new_messages", args=[self.user2.username])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        messages = response.json()["messages"]
        self.assertEqual(messages[0]["sender"], "testuser")
        self.assertEqual(messages[1]["sender"], "testuser2")

        self.assertEqual(messages[0]["content"], "message 1")
        self.assertEqual(messages[1]["content"], "message 2")

    def test_send_message(self):
        self.client.force_login(self.user)
        url = reverse("messaging:send_message", args=[self.user2.username])

        self.assertEqual(Message.objects.count(), 2)

        response = self.client.post(url, {"content": "message 3"})
        self.assertEqual(response.status_code, 200)

        self.assertEqual(Message.objects.count(), 3)
