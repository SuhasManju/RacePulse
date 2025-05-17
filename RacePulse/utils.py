from functools import wraps
from django.utils import timezone
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
import json
from django.conf import settings


TEAM_COLOR_DICT = {
    "alpine": "#00A1E8",
    "aston-martin": "#229971",
    "ferrari": "#E80020",
    "haas": "#B6BABD",
    "kick-sauber": "#52E252",
    "mclaren": "#FF8000",
    "mercedes": "#27F4D2",
    "racing-bulls": "#6692FF",
    "red-bull": "#3671C6",
    "williams": "#1868DB",
}

# Wrapper function that puts every input a single dictionary for ease of use
def CREATE_REQUEST(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        request.TLPOST = {}
        for key, item in kwargs.items():
            request.TLPOST[key] = item

        for key in request.GET:
            request.TLPOST[key] = request.GET.get(key)

        # We want user to see the data of current year
        # if user want to see data of previous year he can select from the dropdown
        if not hasattr(request, "year"):
            year = kwargs.get("year") or 2025
            request.year = year

        return func(view_self, request, *args, **kwargs)

    return wrapper


def CREATE_REQUEST_POST(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        request.TLPOST = {}
        for key, item in kwargs.items():
            request.TLPOST[key] = item

        for key in request.POST:
            request.TLPOST[key] = request.POST.get(key)

        if request.body:
            request.TLPOST.update(**json.loads(request.body))

        return func(view_self, request, *args, **kwargs)

    return wrapper


def combine_datetime(dt, t):
    if not dt or not t:
        return
    x = datetime.strptime(f"{dt} {t}", "%Y-%m-%d %H:%M")
    return timezone.make_aware(x)


def trim_decimal_zeros(value):
    if isinstance(value, (Decimal)):
        return value.normalize()
    return value


def smart_format(value, decimal_places=2):
    try:
        value = Decimal(value).quantize(
            Decimal(f'1.{"0" * decimal_places}'), rounding=ROUND_HALF_UP
        )
        if value == value.to_integral():
            return int(value)
        return float(value)
    except Exception:
        return value


def invert_hex_color(hex_color: str) -> str:
    hex_color = hex_color.lstrip('#')

    # Convert hex to RGB
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Invert each channel
    inverted_r = 255 - r
    inverted_g = 255 - g
    inverted_b = 255 - b

    # Convert back to hex and return formatted string
    return "#{:02x}{:02x}{:02x}".format(inverted_r, inverted_g, inverted_b)


def retrive_latest_race_pk():
    from Race.models import RaceData
    return RaceData.objects.last().race_id
