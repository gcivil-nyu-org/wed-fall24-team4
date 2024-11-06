from django.db import models
from django.contrib.auth.models import User


class Station(models.Model):
    gtfs_stop_id = models.CharField(max_length=10)  # Example: "R01"
    station_id = models.IntegerField()  # Example: "1"
    complex_id = models.IntegerField()  # Example: "1"
    division = models.CharField(max_length=10)  # Example: "BMT"
    line = models.CharField(max_length=50)  # Example: "Astoria"
    stop_name = models.CharField(max_length=255)  # Example: "Astoria-Ditmars Blvd"
    borough = models.CharField(max_length=2)  # Example: "Q"
    cbd = models.BooleanField()  # Example: "FALSE" -> Boolean (convert from string)
    daytime_routes = models.CharField(max_length=20)  # Example: "N W"
    structure = models.CharField(max_length=50)  # Example: "Elevated"
    gtfs_latitude = models.FloatField()  # Example: "40.775036"
    gtfs_longitude = models.FloatField()  # Example: "-73.912034"
    north_direction_label = models.CharField(
        max_length=255, null=True, blank=True
    )  # Example: "Last Stop"
    south_direction_label = models.CharField(
        max_length=255, null=True, blank=True
    )  # Example: "Manhattan"
    ada = models.BooleanField()  # Example: "0" -> Boolean (convert from 0/1)
    ada_northbound = models.BooleanField()  # Example: "0" -> Boolean (convert from 0/1)
    ada_southbound = models.BooleanField()  # Example: "0" -> Boolean (convert from 0/1)

    # Storing geolocation as latitude and longitude fields
    georeference_latitude = models.FloatField()  # Example: 40.775036
    georeference_longitude = models.FloatField()  # Example: -73.912034

    # Optional fields with null values
    ada_notes = models.TextField(null=True, blank=True)  # Example: null

    # Fields with computed values (these might not be necessary to store in your DB)
    computed_region_yamh_8v7k = models.CharField(max_length=10, null=True, blank=True)
    computed_region_wbg7_3whc = models.CharField(max_length=10, null=True, blank=True)
    computed_region_kjdx_g34t = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.stop_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    home_latitude = models.FloatField(null=True, blank=True)
    home_longitude = models.FloatField(null=True, blank=True)
    work_latitude = models.FloatField(null=True, blank=True)
    work_longitude = models.FloatField(null=True, blank=True)
    fav_station = models.ForeignKey(
        Station, on_delete=models.SET_NULL, null=True, blank=True
    )
    fav_source_latitude = models.FloatField(null=True, blank=True)
    fav_source_longitude = models.FloatField(null=True, blank=True)
    fav_dest_latitude = models.FloatField(null=True, blank=True)
    fav_dest_longitude = models.FloatField(null=True, blank=True)
    score = models.IntegerField(default=0)  # reliability score by admin

    def __str__(self):
        return self.user.username


class Review(models.Model):
    station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="rating"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Fair"),
        (3, "3 - Good"),
        (4, "4 - Very Good"),
        (5, "5 - Excellent"),
    ]

    rating = models.IntegerField(choices=RATING_CHOICES)

    class Meta:
        unique_together = [
            "user",
            "station",
        ]  # Enforce uniqueness of user-station combination

    def __str__(self):
        return f"Review by {self.user} on {self.station}"
