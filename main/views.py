# Create your views here.

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from YoutubeAPI import YoutubeAPI
from helpers import get_random_token, get_client_ip
from main.models import User, Playlist, Song

TOKENS = {}


def index(request):
    return render_to_response('../templates/index.html')

def logH(request):
    return render_to_response("../templates/login.html")

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
            user = User.objects.filter(email=email)

            if user and user[0].password == password:
                token = get_random_token()
                TOKENS[token] = user[0]

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
            ip = get_client_ip(request)

            play_list = Playlist.objects.filter(ip=ip)

            if play_list:
                data = play_list[0]

    return JsonResponse({'playlist': data.get_json() if data else None})


@csrf_exempt
def isadmin(request):
    data = None

    if request.method == 'POST':
        token = request.POST.get('token', '')

        if token and token in TOKENS:
            user = TOKENS[token]

            play_list = Playlist.objects.filter(author=user)

            if play_list and play_list[0].ip == get_client_ip(request):
                data = 'yes'
            else:
                data = 'no'

    return JsonResponse({'isadmin': data})


@csrf_exempt
def vote(request):
    status = 403

    if request.method == 'POST':
        token = request.POST.get('token', '')
        song_name = request.POST.get('songname', '')
        vote = request.POST.get('vote', '')

        if token and token in TOKENS:
            ip = get_client_ip(request)
            play_list = Playlist.objects.filter(ip=ip)

            if play_list:
                for s in play_list[0].songs.all():
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

            play_list = Playlist.objects.filter(ip=ip)

            if play_list:
                youtube = YoutubeAPI()
                video_id = youtube.getVideoId(songname)

                if video_id:
                    s = Song(name=songname, rating=1, video_id=video_id)
                    s.save()

                    play_list[0].songs.add(s)

                    status = 200

    return HttpResponse(status=status)

@csrf_exempt
def playnext(request):
    status = 403

    if request.method == 'POST':
        token = request.POST.get('token', '')

        if token and token in TOKENS:
            ip = get_client_ip(request)

            play_list = Playlist.objects.filter(ip=ip)
            if play_list and play_list[0].songs.all().count() > 0:
                cur_song = play_list[0].songs.all().order_by('-rating')[0]
                play_list[0].songs.remove(cur_song)
                play_list[0].save()
                #play_list[0].songs.add(cur_song)

                status = 200

    return HttpResponse(status=status)
