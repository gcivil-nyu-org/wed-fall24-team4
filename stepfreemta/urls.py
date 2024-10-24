from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("app/", include("app.urls", namespace="app")),
    path("admin/", admin.site.urls),
    path("maps/", include("maps.urls", namespace="maps")),
    path("messaging/", include("messaging.urls", namespace="messaging")),
    path("notifications/", include("notifications.urls", namespace="notifications")),
    path("", lambda request: redirect("maps:map_view"), name="landing_page"),
]
