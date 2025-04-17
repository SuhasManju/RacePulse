from functools import wraps
from django.utils import timezone
from datetime import datetime

# Wrapper function that puts every input a single dictionary for ease of use
def CREATE_REQUEST(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        request.TLPOST = {}
        for key, item in kwargs.items():
            request.TLPOST[key] = item

        request.TLPOST.update(request.GET)

        # We want user to see the data of current year
        # if user want to see data of previous year he can select from the dropdown
        if not hasattr(request, "year"):
            year = kwargs.get("year") or 2025
            request.year = year

        return func(view_self, request, *args, **kwargs)

    return wrapper


def combine_datetime(dt, t):
    if not dt or not t:
        return
    x = datetime.strptime(f"{dt} {t}", "%Y-%m-%d %H:%M")
    return timezone.make_aware(x)
