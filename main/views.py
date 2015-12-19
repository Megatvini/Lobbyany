# Create your views here.
import requests
import urllib
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from helpers import get_random_token, get_client_ip
from main.models import User, Playlist, Song, Favorite
from YoutubeAPI import YoutubeAPI

TOKENS = {}


@csrf_exempt
def register(request):
    token = None

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email and password:
            user = User.objects.filter(email=email)

            if not user:
                user = User(email=email, password=password)
                user.save()

                play_list = Playlist()
                play_list.author = user
                play_list.ip = get_client_ip(request)
                play_list.save()

                token = get_random_token()
                TOKENS[token] = user

    return JsonResponse({'token': token})


@csrf_exempt
def login(request):
    token = None

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        token = None

        if email and password:
            user = User.objects.get(email=email)

            if user and user.password == password:
                token = get_random_token()
                TOKENS[token] = user

    return JsonResponse({'token': token})


@csrf_exempt
def logout(request):
    status = 403

    if request.method == 'POST':
        token = request.POST.get('token', '')

        if token:
            if token in TOKENS:
                del TOKENS[token]
                status = 200

    return HttpResponse(status=status)


@csrf_exempt
def getplaylist(request):
    data = None

    if request.method == 'POST':
        token = request.POST.get('token', '')

        if token and token in TOKENS:
            user = TOKENS[token]

            play_list = Playlist.objects.get(author=user)

            if play_list:
                data = play_list

    return JsonResponse({'playlist': data.get_json() if data else None})


@csrf_exempt
def isadmin(request):
    data = None

    if request.method == 'POST':
        token = request.POST.get('token', '')

        if token and token in TOKENS:
            user = TOKENS[token]

            play_list = Playlist.objects.get(author=user)

            if play_list and play_list.ip == get_client_ip(request):
                data = 'yes'
            else:
                data = 'no'

    return JsonResponse({'isadmin': data})


@csrf_exempt
def vote(request):
    status = 403

    if request.POST.method == 'POST':
        token = request.POST.get('token', '')
        song_name = request.POST.get('songname', '')
        vote = request.POST.get('vote', '')

        if token and token in TOKENS:
            ip = get_client_ip(request)
            play_list = Playlist.objects.get(ip=ip)

            if play_list:
                for s in play_list.songs.all():
                    if s.name == song_name:
                        s.rating += 1 if vote == 'up' else -1
                        s.save()

                        user = TOKENS[token]

                        user = User.objects.get(email=user.email)
                        favorite = in_favorits(s, user)

                        update_favorite_rating(favorite, s, user, 4)

                        status = 200
                        break

    return HttpResponse(status=status)


@csrf_exempt
def addsong(request):
    status = 403

    if request.method == 'POST':
        token = request.POST.get('token', '')
        songname = request.POST.get('songname', '')

        if token and songname and token in TOKENS:
            ip = get_client_ip(request)

            play_list = Playlist.objects.get(ip=ip)

            if play_list:
                youtube = YoutubeAPI()
                video_id = youtube.getVideoId(songname)

                if video_id:
                    s = Song(name=songname, rating=0, video_id=video_id)
                    s.save()

                    play_list.songs.add(s)

                    user = TOKENS[token]

                    user = User.objects.get(email=user.email)
                    favorite = in_favorits(s, user)

                    update_favorite_rating(favorite, s, user, 10)

                    status = 200

    return HttpResponse(status=status)


@csrf_exempt
def getFavoriteLobby(request):
    data = None

    if request.method == 'POST':
        token = request.POST.get('token', '')

        if token and token in TOKENS:
            user = TOKENS[token]

            user = User.objects.get(email=user.email)

            play_lists = Playlist.objects.all()

            current_best = 0
            best_play_list = None

            for play_list in play_lists:
                criteria = 0
                for song in play_list.songs.all():
                    favorite = in_favorits(song, user)
                    if favorite is not None:
                        criteria += favorite.points
                if criteria > current_best:
                    current_best = criteria
                    best_play_list = play_lists

            if best_play_list:
                data = best_play_list

    return JsonResponse({'favorite_playlist': data.get_json() if data else None})


def update_favorite_rating(favorite, s, user, point):
    if favorite:
        favorite.points += point / 2
    else:
        favorite = Favorite(song=s, points=point)
        favorite.save()
        user.favorites.add(favorite)


def in_favorits(s, user):
    for favorite in user.favorites.all():
        if favorite.song.name == s.name:
            return favorite
    return None
