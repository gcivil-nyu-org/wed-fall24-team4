from django.shortcuts import render
from .models import Notifications
from reporting.models import Report
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from collections import defaultdict
from .dataclasses import ReportStatusFreqTable, StatusFreqTable


def inbox(request):
    notification_history = Notifications.objects.all().order_by("-timestamp")
    current_time = timezone.now()
    for record in notification_history:
        if current_time - record.timestamp >= timedelta(hours=24):
            record.active = False
            record.save()
    return render(request, "notifications/inbox.html", {})


def get_notifications(request):
    notification_history = Notifications.objects.all().order_by("-timestamp")
    current_time = timezone.now()
    relevant_notifications = []

    for record in notification_history:
        if current_time - record.timestamp >= timedelta(hours=24):
            break
        if record.active:
            relevant_notifications.append(
                {"content": record.content, "timestamp": record.timestamp}
            )
            
    reports = Report.objects.all().order_by("-timestamp")
    active_reports = defaultdict(lambda: ReportStatusFreqTable(
        active=StatusFreqTable(),
        broken=StatusFreqTable(),
        maintenance=StatusFreqTable()
    ))
    for report in reports:
        if current_time - report.timestamp  >= timedelta(hours=4):
            break
        report_key = (report.station,report.infrastructure)
            
        if current_time - report.timestamp  < timedelta(hours=3):
            if report.status == "active":
                active_reports[report_key].active.count += 1
                active_reports[report_key].active.latest_timestamp = report.timestamp
            elif report.status == "broken":
                active_reports[report_key].broken.count += 1
                active_reports[report_key].broken.latest_timestamp = report.timestamp
            elif report.status == "maintenance":
                active_reports[report_key].maintenance.count += 1
                active_reports[report_key].maintenance.latest_timestamp = report.timestamp
            
             
    for report_key in active_reports:
        count, timestamp, status = active_reports[report_key].get_top_status()
        if count >= 3:
            relevant_notifications.append(
                {"content": f"{report_key[0]}'s {report_key[1]} is{" in" if status == 'maintenance' else ""} {status}", "timestamp": timestamp}
            )
        
    return JsonResponse({"notifications": relevant_notifications})
