from __future__ import unicode_literals

import json

import operator
from django.core import serializers
from django.db import models


# Create your models here.

# User
class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)

    def get_json(self):
        pre_data = json.loads(serializers.serialize('json', [self])[1:-1])['fields']
        return json.dumps(pre_data, separators=(',', ':'))

# Song

class Song(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField(default=1)
    video_id = models.CharField(max_length=1000)

    def get_json(self):
        pre_data = json.loads(serializers.serialize('json', [self])[1:-1])['fields']
        return json.dumps(pre_data, separators=(',', ':'))


# Playlist

class Playlist(models.Model):
    author = models.ForeignKey(User)

    ip = models.GenericIPAddressField()
    name = models.CharField(max_length=100)

    songs = models.ManyToManyField(Song, related_name='songs')
    banned_songs = models.ManyToManyField(Song, related_name='banned_songs')

    def get_json(self):
        pre_data = json.loads(serializers.serialize('json', [self])[1:-1])['fields']

        songs = []

        ordered_songs = sorted(self.songs.all(), key=operator.attrgetter('rating'), reverse=True)

        if len(ordered_songs) > 0:
            songs.append(json.loads(ordered_songs[0].get_json()))
            for s in ordered_songs[1:]:
                if s not in self.banned_songs.all():
                    songs.append(json.loads(s.get_json()))
        pre_data['songs'] = songs
        del pre_data['banned_songs']

        pre_data['author'] = self.author.email

        return json.dumps(pre_data, separators=(',', ':'))
