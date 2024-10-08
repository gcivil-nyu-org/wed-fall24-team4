# maps/views.py
import googlemaps
from django.conf import settings
from django.shortcuts import render

def map_view(request):
    # Initialize context with the API key for the template
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    if request.method == 'POST':
        # Get start and end locations from the POST request
        start = request.POST.get('start')
        end = request.POST.get('end')

        # Initialize Google Maps client
        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        try:
            # Fetch directions from Google Maps Directions API
            directions_result = gmaps.directions(start, end, mode="driving")

            # Extract the polyline and steps from the response
            route_polyline = directions_result[0]['overview_polyline']['points']
            route_steps = directions_result[0]['legs'][0]['steps']

            # Add route details to the context for rendering
            context.update({
                'route_polyline': route_polyline,
                'route_steps': route_steps,
                'start': start,
                'end': end,
            })

        except Exception as e:
            # Handle any errors from the API
            context['error'] = str(e)

    # Render the template with the context
    return render(request, 'map.html', context)