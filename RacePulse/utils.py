from functools import wraps
from django.utils import timezone
from datetime import datetime

def CREATE_REQUEST(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        request.TLPOST = {}
        for key, item in kwargs.items():
            request.TLPOST[key] = item
        return func(view_self, request, *args, **kwargs)

    return wrapper


def combine_datetime(dt, t):
    if not dt or not t:
        return
    x = datetime.strptime(f"{dt} {t}", "%Y-%m-%d %H:%M")
    return timezone.make_aware(x)
