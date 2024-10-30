import googlemaps
from django.conf import settings
from django.shortcuts import render
import json
from django.http import JsonResponse
import os
from math import radians, sin, cos, sqrt, atan2
from collections import defaultdict
import heapq


# Load the accessible stations data from the 'data/accessiblemta.json' file
data_path = os.path.join(settings.BASE_DIR, "data", "accessiblemta.json")
with open(data_path, "r") as f:
    subway_data = json.load(f)

# Filter accessible subway stations
accessible_subway_data = [station for station in subway_data if station["ada"] == "1"]


def calculate_distance(lat1, lon1, lat2, lon2):
    # Haversine formula to calculate the distance between two coordinates
    R = 6371  # Earth radius in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) * sin(dlat / 2) + cos(radians(lat1)) * cos(radians(lat2)) * sin(
        dlon / 2
    ) * sin(dlon / 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def find_nearest_accessible_station(lat, lng, max_distance_km=10):
    nearest_station = None
    shortest_distance = float("inf")

    for station in subway_data:
        if station["ada"] == "1":  # Only consider accessible stations
            station_lat = float(station["gtfs_latitude"])
            station_lng = float(station["gtfs_longitude"])
            distance = calculate_distance(lat, lng, station_lat, station_lng)

            if distance <= max_distance_km and distance < shortest_distance:
                shortest_distance = distance
                nearest_station = station

    return nearest_station

# Build station graph based on line connections
def build_station_graph_by_line():
    graph = defaultdict(lambda: defaultdict(list))
    
    for station in accessible_subway_data:
        lines = station["daytime_routes"].split()
        station_id = station["gtfs_stop_id"]

        for line in lines:
            for other_station in accessible_subway_data:
                if station != other_station and line in other_station["daytime_routes"].split():
                    other_station_id = other_station["gtfs_stop_id"]
                    graph[line][station_id].append(other_station_id)
    return graph

station_graph_by_line = build_station_graph_by_line()

def dijkstra_with_line_switching(graph_by_line, start, end, start_line):
    distances = {station: float('inf') for line in graph_by_line for station in graph_by_line[line]}
    previous = {station: (None, None) for line in graph_by_line for station in graph_by_line[line]}
    distances[start] = 0
    pq = [(0, start, start_line)]

    while pq:
        current_distance, current_station, current_line = heapq.heappop(pq)
        if current_station == end:
            break
        
        # Explore neighbors on the same line
        for neighbor in graph_by_line[current_line].get(current_station, []):
            distance = current_distance + 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = (current_station, current_line)
                heapq.heappush(pq, (distance, neighbor, current_line))

        # Explore transfers to other lines at the current station
        for new_line, line_graph in graph_by_line.items():
            if new_line != current_line and current_station in line_graph:
                for neighbor in line_graph[current_station]:
                    distance = current_distance + 1  # Assume transfer cost is 1
                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        previous[neighbor] = (current_station, new_line)
                        heapq.heappush(pq, (distance, neighbor, new_line))

    # Reconstruct path with line details
    path = []
    line_path = []
    current = end
    while current:
        prev, line = previous[current]
        path.insert(0, current)
        line_path.insert(0, line)
        current = prev
    
    return path, line_path

def get_route_with_lines(start_lat, start_lng, end_lat, end_lng):
    start_station = find_nearest_accessible_station(start_lat, start_lng)
    end_station = find_nearest_accessible_station(end_lat, end_lng)

    if not start_station or not end_station:
        return None, None

    start_line = start_station["daytime_routes"].split()[0]  # Choose the first line as starting line
    route, line_path = dijkstra_with_line_switching(station_graph_by_line, start_station["gtfs_stop_id"], end_station["gtfs_stop_id"], start_line)

    # Reformat to station and line data for JavaScript
    route_stations = [
        {
            "name": next(st["stop_name"] for st in accessible_subway_data if st["gtfs_stop_id"] == station_id),
            "lat": float(next(st["gtfs_latitude"] for st in accessible_subway_data if st["gtfs_stop_id"] == station_id)),
            "lng": float(next(st["gtfs_longitude"] for st in accessible_subway_data if st["gtfs_stop_id"] == station_id)),
            "line": line
        }
        for station_id, line in zip(route, line_path)
    ]

    return start_station, route_stations

def fetch_transit_route_with_lines(start_lat, start_lng, end_lat, end_lng):
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    
    # Request directions from Google Maps API with transit mode set to subway
    try:
        directions_result = gmaps.directions(
            origin=(start_lat, start_lng),
            destination=(end_lat, end_lng),
            mode="transit",
            transit_mode="subway"
        )
        
        if not directions_result:
            print("No directions found between the specified points.")
            return None

        # Return the detailed direction steps
        return directions_result[0]  # We only need the first result
        
    except Exception as e:
        print(f"Error fetching transit route: {e}")
        return None

def parse_directions_to_line_segments(directions_result):
    route_segments = []
    
    # Loop through each leg in the directions result
    for leg in directions_result['legs']:
        for step in leg['steps']:
            if step['travel_mode'] == 'TRANSIT' and 'transit_details' in step:
                transit_details = step['transit_details']
                
                # Extract line information
                line_name = transit_details['line']['short_name'] or transit_details['line']['name']
                line_color = transit_details['line'].get('color', '#000000')  # Default to black if color is missing
                
                # Extract station information
                departure_stop = {
                    "name": transit_details['departure_stop']['name'],
                    "lat": transit_details['departure_stop']['location']['lat'],
                    "lng": transit_details['departure_stop']['location']['lng']
                }
                arrival_stop = {
                    "name": transit_details['arrival_stop']['name'],
                    "lat": transit_details['arrival_stop']['location']['lat'],
                    "lng": transit_details['arrival_stop']['location']['lng']
                }

                # Segment data with color coding for the line
                segment = {
                    "line_name": line_name,
                    "line_color": line_color,
                    "departure_stop": departure_stop,
                    "arrival_stop": arrival_stop,
                    "path": step.get('polyline', {}).get('points', '')  # Use safe access
                }
                
                # Append segment to route segments
                route_segments.append(segment)
                
            elif step['travel_mode'] == 'WALKING':
                # Handle walking segments
                walking_segment = {
                    "line_name": "WALKING",
                    "line_color": "#808080",  # Gray color for walking segments
                    "path": step.get('polyline', {}).get('points', '')  # Use safe access
                }
                route_segments.append(walking_segment)
    
    return route_segments

def map_view(request):
    context = {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
        "accessible_subway_data": accessible_subway_data,
    }

    # Optional station location to display on the map
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    station_name = request.GET.get("name")

    if lat and lng and station_name:
        context.update({"lat": lat, "lng": lng, "station_name": station_name})

    # Check if coordinates are provided to find the nearest accessible station
    if lat and lng:
        user_lat = float(lat)
        user_lng = float(lng)
        nearest_station = find_nearest_accessible_station(user_lat, user_lng)

        if nearest_station:
            context.update({
                "nearest_station_name": nearest_station["stop_name"],
                "nearest_station_lat": nearest_station["gtfs_latitude"],
                "nearest_station_lng": nearest_station["gtfs_longitude"],
            })
        else:
            context["nearest_station_error"] = "No accessible station found nearby."

    # Route computation if start and end coordinates are provided
    start_lat = request.GET.get("start_lat")
    start_lng = request.GET.get("start_lng")
    end_lat = request.GET.get("end_lat")
    end_lng = request.GET.get("end_lng")

    if start_lat and start_lng and end_lat and end_lng:
        start_lat, start_lng = float(start_lat), float(start_lng)
        end_lat, end_lng = float(end_lat), float(end_lng)

        # Fetch route using Google Maps Transit Directions API to get line information
        directions = fetch_transit_route_with_lines(start_lat, start_lng, end_lat, end_lng)

        if directions:
            # Parse directions to create line-specific routes with potential transfers
            route_segments = parse_directions_to_line_segments(directions)

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({
                    "route_segments": route_segments
                })
            else:
                context.update({
                    "route_segments": route_segments
                })
        else:
            context["error"] = "No accessible route found."
    # if request.method == "POST":
    #     start = request.POST.get("start")
    #     end = request.POST.get("end")

    #     print("Routing request from:", start, "to:", end)
    #     gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    #     try:
    #         # Fetch directions from Google Maps Directions API using transit mode
    #         directions_result = gmaps.directions(
    #             start, end, mode="transit", transit_mode="subway"
    #         )

    #         route_polyline = directions_result[0]["overview_polyline"]["points"]
    #         route_steps = directions_result[0]["legs"][0]["steps"]

    #         context.update(
    #             {
    #                 "route_polyline": route_polyline,
    #                 "route_steps": route_steps,
    #                 "start": start,
    #                 "end": end,
    #             }
    #         )

        # except Exception as e:
        #     print("Error fetching directions:", str(e))
        #     context["error"] = str(e)

    return render(request, "map.html", context)
