from django.test import TestCase
from importlib import import_module


class WSGITest(TestCase):
    def test_wsgi_application(self):
        try:
            wsgi_module = import_module("stepfreemta.wsgi")
            application = getattr(wsgi_module, "application", None)
            self.assertIsNotNone(application, "WSGI application not found")
        except Exception as e:
            self.fail(f"WSGI application test failed with error: {e}")


class ASGITest(TestCase):
    def test_asgi_application(self):
        try:
            asgi_module = import_module("stepfreemta.asgi")
            application = getattr(asgi_module, "application", None)
            self.assertIsNotNone(application, "ASGI application not found")
        except Exception as e:
            self.fail(f"ASGI application test failed with error: {e}")
