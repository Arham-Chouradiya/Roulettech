from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import requests
import pygeohash as pgh
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify
from django.conf import settings

# Your views will go here

@api_view(['GET'])
@csrf_exempt
def search_events(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    keyword = request.GET.get('keyword')
    radius = request.GET.get('distance')
    category = request.GET.get('category')

    geo_hashed = pgh.encode(float(latitude), float(longitude), precision=7)
    segment_dict = {
        "Default": "",
        "Music": "KZFzniwnSyZfZ7v7nJ",
        "Sports": "KZFzniwnSyZfZ7v7nE",
        "ArtsAndTheatre": "KZFzniwnSyZfZ7v7na",
        "Film": "KZFzniwnSyZfZ7v7nn",
        "Miscellaneous": "KZFzniwnSyZfZ7v7n1"
    }

    segment_id = segment_dict.get(category, "")
    url = f"https://app.ticketmaster.com/discovery/v2/events.json?apikey={settings.TICKETMASTER_API_KEY}&size=20&keyword={keyword}&geoPoint={geo_hashed}&radius={radius}&unit=miles&segmentId={segment_id}"

    response = requests.get(url)
    return JsonResponse(response.json())


@api_view(['GET'])
@csrf_exempt
def suggestions(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        
        url = f"https://app.ticketmaster.com/discovery/v2/suggest?apikey={settings.TICKETMASTER_API_KEY}&keyword={keyword}"
        response = requests.get(url, headers={'Authorization': f'bearer {settings.PRIVATE_API_KEY}'})
        print(response)
        data = response.json()
        return JsonResponse(data)
    

@api_view(['GET'])
@csrf_exempt
def event_details(request):
    event_id = request.query_params.get('event_id')
    
    if not event_id:
        return Response({"error": "event_id is required"}, status=400)

    URL = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json?apikey={settings.TICKETMASTER_API_KEY}"
    
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return Response(response.json())
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
@csrf_exempt
def venue_details(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        
        url = f"https://app.ticketmaster.com/discovery/v2/venues.json?apikey={settings.TICKETMASTER_API_KEY}&keyword={keyword}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Unable to fetch venue details'}, status=response.status_code)
        




@api_view(['GET'])
@csrf_exempt
def spotify_details(request):
    keyword = request.GET.get('keyword')
    
    if not keyword:
        return JsonResponse({'error': 'Keyword parameter is missing'}, status=400)
    
    try:
        # Set up Spotify client with credentials
        spotify = Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET
        ))

        # Search for the artist
        result = spotify.search(q=keyword, type='artist', limit=1)
        
        if result['artists']['items']:
            artist = result['artists']['items'][0]
            return JsonResponse(artist)
        else:
            return JsonResponse({'error': 'Artist not found'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)




@api_view(['GET'])
@csrf_exempt
def spotify_album_details(request):
    keyword = request.GET.get('keyword')
    
    if not keyword:
        return JsonResponse({'error': 'Keyword parameter is missing'}, status=400)
    
    try:
        # Set up Spotify client with credentials
        spotify = Spotify(auth_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIFY_CLIENT_ID,
            client_secret=settings.SPOTIFY_CLIENT_SECRET
        ))

        # Search for the artist's albums
        result = spotify.search(q=keyword, type='artist', limit=1)
        if result['artists']['items']:
            artist_id = result['artists']['items'][0]['id']
            albums = spotify.artist_albums(artist_id, album_type='album', limit=3)
            return JsonResponse(albums['items'], safe=False)
        else:
            return JsonResponse({'error': 'Artist not found'}, status=404)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
