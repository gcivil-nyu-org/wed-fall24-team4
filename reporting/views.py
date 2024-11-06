from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
def reporting_form(request):
    if request.method == "POST":
        current_time = timezone.now()
        form = ReportForm(request.POST)
        if form.is_valid():
            station = form.cleaned_data["station"]
            infrastructure = form.cleaned_data["infrastructure"]
            status = form.cleaned_data["status"]

            # avoid spam by the same user
            latest_report_by_sender = (
                Report.objects.filter(sender=request.user)
                .order_by("-timestamp")
                .first()
            )
            if (
                latest_report_by_sender
                and current_time - latest_report_by_sender.timestamp
                <= timedelta(minutes=20)
            ):
                return redirect("maps:map_view")

            Report.objects.create(
                sender=request.user,
                station=station,
                infrastructure=infrastructure,
                status=status,
            )
            return redirect("maps:map_view")
    else:
        form = ReportForm()

    return render(request, "reporting/reporting_form.html", {"form": form})
