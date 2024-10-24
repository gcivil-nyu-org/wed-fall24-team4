from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import generic
from django.db.models import F
from .models import Station

# User Registration View
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome, {user.username}!")
            return redirect("maps:map_view")
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserCreationForm()

    return render(request, "app/register.html", {"form": form})


# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! You are now logged in.")
            return redirect("maps:map_view")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "app/login.html", {"form": form})


# Logout View
def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("maps:map_view")


# Stations View
class StationsView(generic.ListView):
    model = Station
    template_name = "app/stations.html"
    context_object_name = "station_list"

    def get_queryset(self):
        # Get the search query from the request
        query = self.request.GET.get("q")
        ada_filter = self.request.GET.get("ada_filter")

        # Start with all stations
        queryset = Station.objects.all().order_by(F("stop_name").asc())

        # Apply search filter if applicable
        if query:
            queryset = queryset.filter(stop_name__icontains=query)

        # Apply ADA filter based on the selected option
        if ada_filter == 'fully':
            queryset = queryset.filter(ada=True)
        elif ada_filter == 'partially':
            queryset = queryset.filter(ada_southbound=True, ada_northbound=False)  # or however "partially accessible" is defined
        elif ada_filter == 'not':
            queryset = queryset.filter(ada=False)

        return queryset


# Station Detail View
class StationDetailView(generic.DetailView):
    model = Station
    template_name = "app/station_detail.html"