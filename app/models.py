from django.db import models


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
