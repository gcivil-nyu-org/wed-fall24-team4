from django.urls import path
from . import views

app_name = "app"
urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("stations/", views.StationsView.as_view(), name="stations"),
    path(
        "stations/<int:pk>/", views.StationDetailView.as_view(), name="station_detail"
    ),
]
