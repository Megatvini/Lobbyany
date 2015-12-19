# Create your views here.
import requests
import urllib

import urlfetch as urlfetch
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from helpers import get_random_token, get_client_ip
from main.models import User, Playlist, Song

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
            print token
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

            if play_list:
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

                    url = youtube.getMp3DownloadLink(video_id)

                    r = requests.get(url)
                    # location = r.headers['Location']
                    #
                    # testfile = urllib.URLopener()
                    filename = "main/music/" + songname + ".mp3"
                    # testfile.retrieve(location, filename)

                    with open(filename, "wb") as f:
                        f.write(r.conwtent)

                    s = Song(name=songname, rating=0, url=filename)
                    s.save()

                    play_list.songs.add(s)

                    status = 200

    return HttpResponse(status=status)
