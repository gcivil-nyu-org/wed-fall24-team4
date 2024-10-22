from django.urls import path
from . import views

app_name = "messaging"
urlpatterns = [
    path("inbox", views.inbox, name="inbox"),
    path(
        "direct_messaging/<str:messaging_partner_name>/",
        views.direct_messaging,
        name="direct_messaging",
    ),
    path(
        "send_message/<str:recipient_username>/",
        views.send_message,
        name="send_message",
    ),
    path(
        "get_new_messages/<str:messaging_partner_name>/",
        views.get_new_messages,
        name="get_new_messages",
    ),
]
