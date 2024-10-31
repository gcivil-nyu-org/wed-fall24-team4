from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report
from django.contrib.auth.decorators import login_required


@login_required
def reporting_form(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            station = form.cleaned_data["station"]
            infrastructure = form.cleaned_data["infrastructure"]
            status = form.cleaned_data["status"]
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
