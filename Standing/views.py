from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from RacePulse.utils import CREATE_REQUEST, trim_decimal_zeros
from Race.models import *
from django.db.models import Sum


class CurrentStandingView(View):
    API_RESPONSE = True
    TEMPLATE = ""

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        year = request.TLPOST.get('year')

        driver_standings_qs = SeasonDriverStanding.objects.filter(
            year=year).select_related('driver').order_by('position_number')

        team_standing_qs = SeasonConstructorStanding.objects.filter(
            year=year).select_related('constructor').order_by('position_number')

        engine_standing_qs = SeasonConstructorStanding.objects.filter(year=year).values(
            'engine_manufacturer', 'engine_manufacturer__name').annotate(c_points=Sum('points')).order_by('-c_points')

        driver_data = []
        for d in driver_standings_qs:
            i = {
                'position': d.position_number,
                'driverName': d.driver.name,
                'points': trim_decimal_zeros(d.points),
            }
            driver_data.append(i)

        context_dict['driverData'] = driver_data

        team_data = []
        for c in team_standing_qs:
            i = {
                'position': c.position_number,
                'teamName': c.constructor.name,
                'points': trim_decimal_zeros(c.points),
            }
            team_data.append(i)

        context_dict['teamData'] = team_data

        engine_data = []
        for postion, e in enumerate(engine_standing_qs):
            i = {
                'postion': postion,
                'engineName': e['engine_manufacturer__name'],
                'points': trim_decimal_zeros(e['c_points']),
            }
            engine_data.append(i)

        context_dict['engineData'] = engine_data

        if self.API_RESPONSE:
            return JsonResponse(context_dict)
