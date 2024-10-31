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
