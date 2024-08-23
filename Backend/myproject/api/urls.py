from django.urls import path
from .views import search_events, suggestions, event_details, venue_details, spotify_details, spotify_album_details

urlpatterns = [
    path('search_events/', search_events),
    path('suggestions/', suggestions),
    path('event_details/', event_details),  
    path('venue_details/', venue_details),
    path('spotify_details/', spotify_details),
    path('spotify_album_details/', spotify_album_details),
]
