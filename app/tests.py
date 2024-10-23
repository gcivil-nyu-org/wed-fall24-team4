from django.test import TestCase
from django.urls import reverse
from .models import Station
from django.contrib.auth.models import User
from django.conf import settings
import json


class LoginViewTest(TestCase):
    def setUp(self):
        self.url = reverse("app:login")
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_login_view_get(
        self,
    ):  # accessed via a GET request, check status code is 200 and correct template (app/login.html) is used # noqa: E501
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/login.html")

    def test_login_view_post_success(
        self,
    ):  # It asserts that the response redirects the user to the map view upon successful login # noqa: E501
        response = self.client.post(
            self.url, {"username": "testuser", "password": "password"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("maps:map_view"))

    def test_login_view_post_failure(
        self,
    ):  # simulates a login attempt with incorrect credentials via a POST request, asserts that the page reloads (status code 200) and checks for the presence of the error message # noqa: E501
        response = self.client.post(
            self.url, {"username": "wronguser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, 200)
        # Instead of asserting form error, check for error message presence
        self.assertContains(response, "Please enter a correct username and password.")


class RegisterViewTest(TestCase):
    def setUp(self):
        self.url = reverse("app:register")

    def test_register_view_get(
        self,
    ):  # accessed via a GET request, check status code is 200 and correct template (app/register.html) is used # noqa: E501
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app/register.html")

    def test_register_view_post_success(
        self,
    ):  # simulates a registration attempt with valid data (matching passwords) and redirects the user to the map view upon successful registtration # noqa: E501
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("maps:map_view"))

    def test_register_view_post_failure(
        self,
    ):  # simulates a registration attempt where the two password fields do not match
        response = self.client.post(
            self.url,
            {
                "username": "newuser",
                "password1": "testpassword",
                "password2": "differentpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        # Instead of asserting form error, check for error message presence
        self.assertContains(response, "The two password fields didn’t match.")


class StationsAccessibilityTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Load stations from accessiblemta.json
        with open(settings.BASE_DIR / "data/accessiblemta.json", "r") as f:
            stations_data = json.load(f)

        # Create station objects in the test database
        for station in stations_data:
            Station.objects.create(
                gtfs_stop_id=station["gtfs_stop_id"],
                station_id=station["station_id"],
                complex_id=station["complex_id"],
                division=station["division"],
                line=station["line"],
                stop_name=station["stop_name"],
                borough=station["borough"],
                cbd=station["cbd"] == "TRUE",
                daytime_routes=station["daytime_routes"],
                structure=station["structure"],
                gtfs_latitude=float(station["gtfs_latitude"]),
                gtfs_longitude=float(station["gtfs_longitude"]),
                ada=station["ada"] == "1",
                ada_northbound=station["ada_northbound"] == "1",
                ada_southbound=station["ada_southbound"] == "1",
                georeference_latitude=float(station["georeference"]["coordinates"][1]),
                georeference_longitude=float(station["georeference"]["coordinates"][0]),
            )

    def test_station_accessibility(self):
        # Test for a station marked as accessible
        station = Station.objects.get(
            gtfs_stop_id="R03"
        )  # Example: Astoria Blvd is ADA accessible
        response = self.client.get(reverse("app:station_detail", args=[station.id]))
        self.assertContains(response, "Accessible: True")

        # Test for a station not marked as accessible
        station = Station.objects.get(
            gtfs_stop_id="R01"
        )  # Example: Astoria-Ditmars Blvd is not ADA accessible
        response = self.client.get(reverse("app:station_detail", args=[station.id]))
        self.assertContains(response, "Accessible: False")

    def test_go_button_redirect(self):
        # Test clicking the "Go" button and ensure correct redirection to map view with coordinates # noqa: E501
        station = Station.objects.get(gtfs_stop_id="R03")  # Example: Astoria Blvd
        response = self.client.get(reverse("app:station_detail", args=[station.id]))
        go_button_url = (
            reverse("maps:map_view")
            + f"?lat={station.gtfs_latitude}&lng={station.gtfs_longitude}&name={station.stop_name}"  # noqa: E501
        )

        self.assertContains(response, f'href="{go_button_url}"')
