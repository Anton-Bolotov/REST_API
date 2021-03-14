from django.urls import path
from .views import *

app_name = 'rest_api'

urlpatterns = [
    path('search/<str:track_name>/', MusicSearch.as_view()),
    path('search/<str:track_name>/track_id/<int:track_id>/', MusicAddIntoDB.as_view()),
    path('search/<str:track_name>/page/<int:page_id>/', MusicSearch.as_view()),
    path('search/<str:track_name>/page/<int:page_id>/track_id/<int:track_id>/', MusicAddIntoDB.as_view()),
    path('search/<str:track_name>/<str:artist_name>/', MusicSearch.as_view()),
    path('search/<str:track_name>/<str:artist_name>/track_id/<int:track_id>/', MusicAddIntoDB.as_view()),
    path('search/<str:track_name>/<str:artist_name>/page/<int:page_id>/', MusicSearch.as_view()),
    path('search/<str:track_name>/<str:artist_name>/page/<int:page_id>/track_id/<int:track_id>/', MusicAddIntoDB.as_view()),
    path('event/', CreateEvent.as_view()),
    path('event/<str:event_name>/', CreateEvent.as_view()),
    path('music-to-event/<str:event_name>/', AddMusicToEvent.as_view()),
    path('event/<str:event_name>/suggestions/', TopList.as_view()),
    path('event/<str:event_name>/suggestions/<str:track_name>/', TopList.as_view()),
]
