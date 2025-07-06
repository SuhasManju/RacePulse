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

random_colours = [
    "#A0522D",  # Sienna
    "#FFD700",  # Gold
    "#6A0DAD",  # Purple
    "#008080",  # Teal
    "#DC143C",  # Crimson
    "#4B0082",  # Indigo
    "#FF1493",  # Deep Pink
    "#8B4513",  # Saddle Brown
    "#00CED1",  # Dark Turquoise
    "#FF4500",  # Orange Red
]


# Wrapper function that puts every input a single dictionary for ease of use
def CREATE_REQUEST(func):
    @wraps(func)
    def wrapper(view_self, request, *args, **kwargs):
        request.TLPOST = {}
        for key, item in kwargs.items():
            request.TLPOST[key] = item

        for key in request.GET:
            ans_list = request.GET.getlist(key)
            ans = request.GET.get(key)
            if len(ans_list) <= 1:
                request.TLPOST[key] = ans
            else:
                request.TLPOST[key] = ans_list

        # We want user to see the data of current year
        # if user want to see data of previous year he can select from the dropdown
        year = kwargs.get("year") or request.session.get(
            "year") or settings.CURRENT_YEAR
        request.session['year'] = year

        request.year = request.session['year']

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


def retrive_driver_list(year: int):
    from Race.models import SeasonDriver
    driver_list = SeasonDriver.objects.filter(
        year_id=year).values_list("driver_id", "driver__name")
    return list(driver_list)


def retrive_team_list(year: int):
    from Race.models import SeasonConstructor

    team_list = SeasonConstructor.objects.filter(
        year_id=year).values_list("constructor_id", "constructor__name")
    return list(team_list)
