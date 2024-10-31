from django.contrib.auth.models import User
from django.db import models


def get_station_choices():
    import json

    with open("data/accessiblemta.json", "r") as file:
        data = json.load(file)

    station_names = list(set([x["stop_name"] for x in data]))
    return [(str(x).upper(), str(x)) for x in station_names]


class Infrastructure(models.TextChoices):
    RAMP = "ramp"
    ELEVATOR = "elevator"
    ESCALATOR = "escalator"


class Status(models.TextChoices):
    ACTIVE = "active"
    BROKEN = "broken"
    MAINTENANCE = "maintenance"


class Report(models.Model):
    sender = models.ForeignKey(User, related_name="report", on_delete=models.CASCADE)
    station = models.CharField(choices=get_station_choices(), max_length=40)
    infrastructure = models.CharField(choices=Infrastructure.choices, max_length=9)
    status = models.CharField(choices=Status.choices, max_length=11)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report from {self.sender} about {self.station}'s \
            {self.infrastructure}'s status being {self.status} at {self.timestamp}"
