import random
import string


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip


def get_random_token():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
