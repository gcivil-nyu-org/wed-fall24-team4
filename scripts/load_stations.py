import json
from app.models import Station


def load_json_to_db(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)  # Load the entire JSON array

    for entry in data:
        station = Station(
            gtfs_stop_id=entry["gtfs_stop_id"],
            station_id=int(
                entry["station_id"]
            ),  # Consider adding try-except for safety
            complex_id=int(entry["complex_id"]),
            division=entry["division"],
            line=entry["line"],
            stop_name=entry["stop_name"],
            borough=entry["borough"],
            cbd=(entry["cbd"].lower() == "true"),  # Convert string to boolean correctly
            daytime_routes=entry["daytime_routes"],
            structure=entry["structure"],
            gtfs_latitude=float(entry["gtfs_latitude"]),
            gtfs_longitude=float(entry["gtfs_longitude"]),
            north_direction_label=entry.get("north_direction_label", None),
            south_direction_label=entry.get("south_direction_label", None),
            ada=(entry["ada"] == "1"),
            ada_northbound=(entry["ada_northbound"] == "1"),
            ada_southbound=(entry["ada_southbound"] == "1"),
            georeference_latitude=entry.get("georeference", {}).get(
                "coordinates", [None, None]
            )[1],
            georeference_longitude=entry.get("georeference", {}).get(
                "coordinates", [None, None]
            )[0],
            ada_notes=entry.get("ada_notes", None),
            computed_region_yamh_8v7k=entry.get(":@computed_region_yamh_8v7k", None),
            computed_region_wbg7_3whc=entry.get(":@computed_region_wbg7_3whc", None),
            computed_region_kjdx_g34t=entry.get(":@computed_region_kjdx_g34t", None),
        )
        station.save()  # Save each station object to the database
