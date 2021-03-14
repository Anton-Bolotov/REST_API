import datetime

from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .logic import search_music
from .models import *
from .serializers import MusicListSerializer, AddMusicToEventSerializer
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MusicSearch(APIView):
    """ Класс для поиска треков """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, track_name, artist_name=None, page_id=None):
        """ Получить все треки по названию песни и/или имени артиста с
                возможностью перехода по страницам стороннего API """
        result = search_music(track_name=track_name, artist_name=artist_name, page_id=page_id)
        return Response(result)


class MusicAddIntoDB(APIView):
    """ Класс для работы с треками """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, track_name, artist_name=None, page_id=None, track_id=None):
        """ Посмотреть все треки по определенным критериям / определенный трек """
        result = search_music(track_name=track_name, artist_name=artist_name, page_id=page_id, track_id=track_id)
        return Response(result)

    def post(self, request, track_name, track_id, artist_name=None, page_id=None):
        """ Добавить трек в базу по track_id """
        result = search_music(track_name=track_name, track_id=track_id, artist_name=artist_name, page_id=page_id)
        if not AllMusic.objects.filter(track_name=result['name']).exists():
            add_music = AllMusic(track_name=result['name'], artist=result['artist'], url=result['url'], views=result['listeners'])
            add_music.save(result['name'])
            return Response({'success': f'Трек "{result["name"]}" успешно добавлен'})
        else:
            return Response({'error': f'Трек "{result["name"]}" уже в базе'})


class CreateEvent(APIView):
    """ Класс для управления эвентами """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, event_name=None):
        """ Посмотреть все эвенты / определенный эвент """
        events = Events.objects.all()
        if event_name:
            events = Events.objects.filter(event_name=event_name)
        serializer = MusicListSerializer(events, many=True)
        return Response({'events': serializer.data})

    def post(self, request, event_name=None):
        """ Создать эвент """
        events = request.data.get('events')
        if not Events.objects.filter(event_name=events['event_name']).exists():
            if events['finish_date'] < events['start_date']:
                return Response({'error': 'Дата окончания не может быть раньше даты начала эвента'})
            serializer = MusicListSerializer(data=events)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'success': f'Эвент "{events["event_name"]}" успешно добавлен'})
        else:
            return Response({'error': f'Эвент c таким именем "{events["event_name"]}" существует'})

    def delete(self, request, event_name=None):
        """ Удалить эвент """
        if not event_name:
            return Response({'error': 'Пожалуйста укажите название эвента в запросе'})
        if Events.objects.filter(event_name=event_name).exists():
            event = Events.objects.filter(event_name=event_name)
            event.delete()
            return Response({'success': f'Эвент "{event_name}" успешно удален'})
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})

    def put(self, request, event_name=None):
        """ Обновить эвент """
        data = request.data.get('events')
        if Events.objects.filter(event_name=data['event_name']).exists():
            event = Events.objects.filter(event_name=data['event_name'])
            if data['finish_date'] < data['start_date']:
                return Response({'error': 'Дата окончания не может быть раньше даты начала эвента'})
            serializer = MusicListSerializer(instance=event, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            return Response({'success': f'Эвент "{event_name}" успешно обновлен'})
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})


class AddMusicToEvent(APIView):
    """ Класс для работы с плейлистами """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, event_name):
        """ получение треков, входящих в плейлист (по убыванию просмотров) """
        if Events.objects.filter(event_name=event_name).exists():
            event_pk = Events.objects.get(event_name=event_name).pk
            events = MusicOnPlaylist.objects.filter(playlist_name=event_pk).order_by('-views')
            serializer = AddMusicToEventSerializer(events, many=True)
            return Response({'events': serializer.data})
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})

    def post(self, request, event_name):
        """ Добавление в плейлист """
        events = request.data.get('events')
        if Events.objects.filter(event_name=event_name).exists():
            event_data = Events.objects.get(event_name=event_name)

            current_count_tracks = MusicOnPlaylist.objects.filter(playlist_name=event_data).count()
            max_tracks = event_data.max_tracks
            if current_count_tracks >= max_tracks:
                return Response({'error': 'Лимит треков превышен'})

            start_date = event_data.start_date
            finish_date = event_data.finish_date
            now_date = datetime.datetime.now(datetime.timezone.utc)
            if start_date <= now_date <= finish_date:
                playlist = MusicOnPlaylist(
                    track_name=events['track_name'],
                    artist=events['artist'],
                    url=events['url'],
                    views=events['views'],
                    playlist_name=event_data
                )
                playlist.save()
                return Response({'success': f'Трек "{events["track_name"]}" успешно добавлен в плейлист "{event_name}"'})

            elif now_date > finish_date:
                return Response({'error': 'Эвент уже закончился'})
            else:
                return Response({'error': 'Эвент еще не начался'})
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})

    def delete(self, request, event_name):
        """ Удалить плейлист """
        if Events.objects.filter(event_name=event_name).exists():
            event = Events.objects.filter(event_name=event_name)
            event.delete()
            return Response({'success': f'Эвент "{event_name}" успешно удален'})
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})


class TopList(APIView, PageNumberPagination):
    """ Класс для музыкальных предложений """
    page_size = 5
    max_page_size = 1000
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, event_name, track_name=None):
        """ Получение текущих предложений для плейлиста (по убыванию просмотров)
                            с пагинацией страниц """
        if Events.objects.filter(event_name=event_name).exists():

            bad_list = []
            event_pk = Events.objects.get(event_name=event_name).pk
            queryset_music = MusicOnPlaylist.objects.filter(playlist_name=event_pk)
            for item in queryset_music:
                bad_list.append(item)

            music = AllMusic.objects.exclude(track_name__in=bad_list).order_by('-views')

            if music.count() == 0:
                return Response({'error': f'Для эвента c таким именем "{event_name}" '
                                f'отсутствуют предложения в базе, пожалуйста добавьте треки в базу через поиск'})
            if track_name:
                music = AllMusic.objects.get(track_name=track_name)
                serializer = AddMusicToEventSerializer(instance=music)
                return Response({'events': serializer.data})

            paginate_queryset = self.paginate_queryset(music, self.request)
            serializer = AddMusicToEventSerializer(instance=paginate_queryset, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})

    def post(self, request, event_name, track_name):
        """ Возможность разового голоса "за" какой-то из предложенных для плейлиста треков """
        if Events.objects.filter(event_name=event_name).exists():
            event = Events.objects.get(event_name=event_name)
            music = AllMusic.objects.get(track_name=track_name)

            current_count_tracks = MusicOnPlaylist.objects.filter(playlist_name=event).count()
            max_tracks = event.max_tracks
            if current_count_tracks >= max_tracks:
                return Response({'error': 'Лимит треков для этого плейлиста превышен'})

            start_date = event.start_date
            finish_date = event.finish_date
            now_date = datetime.datetime.now(datetime.timezone.utc)
            if start_date <= now_date <= finish_date:
                add_to_playlist = MusicOnPlaylist(
                    track_name=music.track_name,
                    artist=music.artist,
                    url=music.url,
                    views=music.views,
                    playlist_name=event
                )
                add_to_playlist.save()
                return Response({'success': f'Трек {music.track_name} успешно добавлен в Эвент "{event_name}"'})
            elif now_date > finish_date:
                return Response({'error': 'Эвент уже закончился'})
            else:
                return Response({'error': 'Эвент еще не начался'})
        else:
            return Response({'error': f'Эвент c таким именем "{event_name}" отсутствует в базе'})
