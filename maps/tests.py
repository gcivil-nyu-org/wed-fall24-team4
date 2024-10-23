from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.conf import settings
from django.contrib.auth.models import User


class MapsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("maps:map_view")
        self.valid_data = {
            "start": "Times Square, New York, NY",
            "end": "Central Park, New York, NY",
        }

    def test_template_used(
        self,
    ):  # checks if the correct template map.html is used when accessing the map view via a GET request. asserts that the status code is 200 and the correct template is rendered # noqa: E501
        """Test that the map template is rendered correctly."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "map.html")
        self.assertEqual(response.status_code, 200)

    @patch("googlemaps.Client.directions")
    # Mocks the Google Maps API’s directions method to return a simulated successful response. checks that the API is called with the expected parameters # noqa: E501
    # It also asserts that the route information (mock_polyline, steps) is correctly included in the response context. # noqa: E501
    def test_directions_success(self, mock_directions):
        """Test the successful retrieval of directions."""
        # Mock a successful API response
        mock_directions.return_value = [
            {
                "overview_polyline": {"points": "mock_polyline"},
                "legs": [
                    {
                        "steps": [
                            {
                                "distance": {"text": "0.1 mi"},
                                "instructions": "Head north",
                            }
                        ]
                    }
                ],
            }
        ]

        response = self.client.post(self.url, self.valid_data)

        # Check if the mock was called with expected parameters
        mock_directions.assert_called_once_with(
            "Times Square, New York, NY",
            "Central Park, New York, NY",
            mode="transit",
            transit_mode="subway",
        )

        # Ensure the context contains the expected values
        self.assertEqual(response.context["route_polyline"], "mock_polyline")
        self.assertEqual(len(response.context["route_steps"]), 1)
        self.assertEqual(
            response.context["route_steps"][0]["distance"]["text"], "0.1 mi"
        )

    @patch("googlemaps.Client.directions")
    def test_directions_api_error(
        self, mock_directions
    ):  # make the mocked directions method raise an exception. checks that the response contains the error message "API Error" in the context when the API call fails # noqa: E501
        """Test that API errors are handled properly."""
        mock_directions.side_effect = Exception("API Error")

        response = self.client.post(self.url, self.valid_data)

        # Check that the error message is present in the context
        self.assertIn("error", response.context)
        self.assertEqual(response.context["error"], "API Error")

    def test_missing_start_or_end(
        self,
    ):  # checks if submitting a form without a starting point or an ending point results in an appropriate error message and make sure the error message is present # noqa: E501
        """Test that missing start or end location returns an error."""
        response = self.client.post(
            self.url, {"start": "", "end": "Central Park, New York, NY"}
        )
        self.assertContains(
            response, "Please enter both a starting point and an ending point."
        )

        response = self.client.post(
            self.url, {"start": "Times Square, New York, NY", "end": ""}
        )
        self.assertContains(
            response, "Please enter both a starting point and an ending point."
        )

    def test_google_maps_api_key_in_context(
        self,
    ):  # checks if the Google Maps API key is passed to the template context when the map view is accessed via a GET request # noqa: E501
        """Test that the Google Maps API key is passed to the template context."""
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["google_maps_api_key"], settings.GOOGLE_MAPS_API_KEY
        )


class ButtonsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("maps:map_view")
        self.login_url = reverse("app:login")
        self.register_url = reverse("app:register")
        # Create a user to log in
        self.user = User.objects.create_user(username="testuser", password="password")

    def test_login_button_exists(self):
        # Checks that login button exists on map page
        response = self.client.get(self.url)
        self.assertContains(
            response, "<button>Login</button>", html=True
        )  # Check if the button is in the page # noqa: E501

    def test_login_button_redirect(self):
        # Checks that pressing login button redirects to login screen
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Ensure map page loads correctly

        # Simulate logging in by posting credentials to the login view
        response = self.client.post(
            self.login_url, {"username": "testuser", "password": "password"}
        )  # noqa: E501
        self.assertEqual(response.status_code, 302)  # Redirection status code
        self.assertRedirects(
            response, reverse("maps:map_view")
        )  # Test the correct redirect back to map view # noqa: E501

    def test_register_button_exists(self):
        # Checks register button exists
        response = self.client.get(self.url)
        self.assertContains(response, '<button>Register</button>', html=True)  # Check if register button is on page

    def test_register_button_redirects(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        reponse = self.client.post(self.register_url, {"username": "testuser", "password": "password"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('maps:map_view'))
