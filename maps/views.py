import googlemaps
from django.conf import settings
from django.shortcuts import render

def map_view(request):
    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    }

    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')

        gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

        try:
            # Fetch directions from Google Maps Directions API using transit mode
            directions_result = gmaps.directions(start, end, mode="transit", transit_mode="subway")

            route_polyline = directions_result[0]['overview_polyline']['points']
            route_steps = directions_result[0]['legs'][0]['steps']

            context.update({
                'route_polyline': route_polyline,
                'route_steps': route_steps,
                'start': start,
                'end': end,
            })

        except Exception as e:
            context['error'] = str(e)

    return render(request, 'map.html', context)