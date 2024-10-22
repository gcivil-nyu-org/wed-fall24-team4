from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.views import generic
from django.db.models import F
from .models import Station


# home view
def home_view(request):
    return render(request, "app/home.html", {})


# User Registration View
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user to the database
            login(request, user)  # Automatically log the user in after registration
            messages.success(
                request, f"Account created successfully! Welcome, {user.username}!"
            )
            return redirect("maps:map_view")
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserCreationForm()  # Display an empty form if the request is not POST

    return render(request, "app/register.html", {"form": form})


# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(
                request, f"Welcome, {user.username}! You are now logged in."
            )
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
    context_object_name = "station_list"  # To reference the object in your template

    def get_queryset(self):
        # Get the search query from the request (GET parameter)
        query = self.request.GET.get("q")

        # If there's a search query, filter stations based on the name
        if query:
            return Station.objects.filter(stop_name__icontains=query).order_by(
                F("stop_name").asc()
            )
        else:
            # Otherwise, return all stations ordered by name
            return Station.objects.all().order_by(F("stop_name").asc())


# Station Detail View
class StationDetailView(generic.DetailView):
    model = Station
    template_name = "app/station_detail.html"
