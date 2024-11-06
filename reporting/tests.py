from django.test import TestCase, Client
from django.urls import reverse
from .models import Report
from django.contrib.auth.models import User


class ReportingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword@1234"
        )
        self.user_list = [
            User.objects.create_user(
                username=f"testuser{x}", password="testpassword@1234"
            )
            for x in range(1, 12)
        ]

    def test_inbox_view_get(self):
        self.client.force_login(self.user)
        url = reverse("reporting:reporting_form")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "reporting/reporting_form.html")

    def test_send_report(self):
        self.client.force_login(self.user)
        url = reverse("reporting:reporting_form")
        self.assertEqual(Report.objects.count(), 0)
        response = self.client.post(
            url, {"station": "191 ST", "infrastructure": "elevator", "status": "active"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 1)

    def test_auto_broadcast(self):

        url = reverse("reporting:reporting_form")
        for x in self.user_list[:3]:
            self.client.force_login(x)
            response = self.client.post(
                url,
                {"station": "191 ST", "infrastructure": "elevator", "status": "broken"},
            )
            self.client.logout()

        url = reverse("notifications:get_notifications")
        response = self.client.get(url)
        data = response.json()["notifications"]
        self.assertEqual(data[0]["content"], "191 ST's elevator is broken")

        url = reverse("reporting:reporting_form")
        for x in self.user_list[3:6]:
            self.client.force_login(x)
            response = self.client.post(
                url,
                {"station": "191 ST", "infrastructure": "elevator", "status": "active"},
            )
            self.client.logout()

        url = reverse("notifications:get_notifications")
        response = self.client.get(url)
        data = response.json()["notifications"]
        self.assertEqual(data[0]["content"], "191 ST's elevator is active")

        url = reverse("reporting:reporting_form")
        for x in self.user_list[6:8]:
            self.client.force_login(x)
            response = self.client.post(
                url,
                {
                    "station": "191 ST",
                    "infrastructure": "elevator",
                    "status": "maintenance",
                },
            )
            self.client.logout()

        url = reverse("notifications:get_notifications")
        response = self.client.get(url)
        data = response.json()["notifications"]
        self.assertEqual(data[0]["content"], "191 ST's elevator is active")

        url = reverse("reporting:reporting_form")
        for x in self.user_list[8:]:
            self.client.force_login(x)
            response = self.client.post(
                url,
                {
                    "station": "191 ST",
                    "infrastructure": "elevator",
                    "status": "maintenance",
                },
            )
            self.client.logout()

        url = reverse("notifications:get_notifications")
        response = self.client.get(url)
        data = response.json()["notifications"]
        self.assertEqual(data[0]["content"], "191 ST's elevator is in maintenance")
