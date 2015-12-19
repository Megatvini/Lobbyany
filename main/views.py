# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from main.models import User, Playlist
from helpers import get_random_token, get_client_ip

TOKENS = set()


@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        status = 403

        if email and password:
            user = User(email=email, password=password)
            user.save()

            play_list = Playlist()
            play_list.author = user
            play_list.ip = get_client_ip(request)
            play_list.save()

            status = 200

    return HttpResponse(status=status)


@csrf_exempt
def login(request):
    token = None

    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        token = None

        if email and password:
            user = User.objects.get(email=email)

            if user.password == password:
                token = get_random_token()
                TOKENS.add(token)

    return JsonResponse({'token': token})

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')

        status = 403

        if token:
            TOKENS.remove(token)
            status = 200

    return HttpResponse(status=status)