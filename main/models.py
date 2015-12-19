from __future__ import unicode_literals
from django.db import models


# Create your models here.

# User
class User(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=16)


# Playlist

class Playlist(models.Model):

    author = models.ForeignKey(User)

    ip = models.IPAddressField()
    name = models.CharField(max_length=100)

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    songs = models.ManyToManyField(Song)
    banned_songs = models.ManyToManyField(Song)


# Song

class Song(models.Model):
    name = models.URLField()
    rating = models.ImageField(default=0)

