from django.urls import path
from . import views

app_name = "notifications"
urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("get_notifications/", views.get_notifications, name="get_notifications"),
]
