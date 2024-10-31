from django.urls import path
from . import views

app_name = "reporting"
urlpatterns = [
    path("reporting_form", views.reporting_form, name="reporting_form"),
]
