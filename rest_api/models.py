from django.db import models


class AllMusic(models.Model):
    track_name = models.CharField(max_length=100, unique=True, verbose_name='Название музыки')
    artist = models.CharField(max_length=100, verbose_name='Исполнитель')
    url = models.URLField(max_length=400, unique=True, verbose_name='Ссылка на музыку')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def __str__(self):
        return self.track_name

    class Meta:
        verbose_name = 'Вся Музыка'
        verbose_name_plural = 'Вся Музыка'
        ordering = ['-views']


class MusicOnPlaylist(models.Model):
    track_name = models.CharField(max_length=100, verbose_name='Название музыки')
    artist = models.CharField(max_length=100, verbose_name='Исполнитель')
    url = models.URLField(max_length=400, verbose_name='Ссылка на музыку')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    add_to_playlist = models.DateField(auto_now_add=True, verbose_name='Дата добавления')
    playlist_name = models.ForeignKey('Events', on_delete=models.PROTECT, verbose_name='Название плейлиста')

    def __str__(self):
        return self.track_name

    class Meta:
        verbose_name = 'Музыка в плейлисте'
        verbose_name_plural = 'Музыка в плейлистах'
        ordering = ['-add_to_playlist']


class Events(models.Model):
    event_name = models.CharField(max_length=100, unique=True, verbose_name='Название эвента')
    start_date = models.DateTimeField(verbose_name='Дата начала приема музыки')
    finish_date = models.DateTimeField(verbose_name='Дата окончания приема музыки')
    max_tracks = models.IntegerField(default=20, verbose_name='Максимальное количество треков')

    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = 'Эвент'
        verbose_name_plural = 'Эвента'
