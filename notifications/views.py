from django.shortcuts import render
from .models import Notifications
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse


def inbox(request):
    return render(request, "notifications/inbox.html", {})


def get_notifications(request):
    notification_history = Notifications.objects.values().order_by("-timestamp")
    current_time = timezone.now()
    relevant_notifications = []

    for record in notification_history:
        if current_time - record["timestamp"] >= timedelta(hours=24):
            break
        if record["active"]:
            relevant_notifications.append(
                {"content": record["content"], "timestamp": record["timestamp"]}
            )

    return JsonResponse({"notifications": relevant_notifications})
