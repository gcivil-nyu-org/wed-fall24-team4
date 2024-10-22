from django.test import TestCase
from django.urls import reverse
from .models import Station
from django.contrib.auth.models import User


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


class StationsViewTest(TestCase):
    def setUp(self):
        # Create a sample Station object with all required fields filled.
        self.station = Station.objects.create(
            gtfs_stop_id="R01",
            station_id=1,
            complex_id=1,
            division="BMT",
            line="Astoria",
            stop_name="Astoria-Ditmars Blvd",
            borough="Q",
            cbd=False,
            daytime_routes="N W",
            structure="Elevated",
            gtfs_latitude=40.775036,
            gtfs_longitude=-73.912034,
            ada=True,
            ada_northbound=True,
            ada_southbound=True,
            georeference_latitude=40.775036,
            georeference_longitude=-73.912034,
        )

    def test_stations_view(
        self,
    ):  # checks if the stations list page loads successfully and includes data from a sample Station object created in setUp, asserts that the page returns status code 200 and contains the stop name of the sample station # noqa: E501
        response = self.client.get(reverse("app:stations"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.station.stop_name)
