from rest_framework import serializers
from .models import Events, MusicOnPlaylist


class MusicListSerializer(serializers.Serializer):
    event_name = serializers.CharField()
    start_date = serializers.DateTimeField()
    finish_date = serializers.DateTimeField()
    max_tracks = serializers.IntegerField()

    def create(self, validated_data):
        return Events.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.event_name = validated_data.get('event_name')
        instance.start_date = validated_data.get('start_date')
        instance.finish_date = validated_data.get('finish_date')
        instance.max_tracks = validated_data.get('max_tracks')
        return instance


class AddMusicToEventSerializer(serializers.Serializer):
    track_name = serializers.CharField()
    artist = serializers.CharField()
    url = serializers.URLField()
    views = serializers.IntegerField()

    def create(self, validated_data):
        return MusicOnPlaylist.objects.create(**validated_data)
