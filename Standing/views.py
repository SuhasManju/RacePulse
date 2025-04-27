from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from RacePulse.utils import CREATE_REQUEST, trim_decimal_zeros
from Race.models import *
from django.db.models import Sum, F, Window
import pandas as pd
import numpy as np

class CurrentStandingView(View):
    API_RESPONSE = True
    template = ""

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


class CurrentStandingGraphView(View):
    API_RESPONSE = True
    TEMpdATE = ""

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}

        year = request.TLPOST.get('year')
        columns = ['driver_id', 'driver__name', 'c_points',
                   'race__grand_prix__abbreviation', 'race_id', 'driver__abbreviation']

        driver_standing_qs = RaceData.objects.filter(
            race__year=year, type__in=[RaceData.SPRINT_RACE_RESULT, RaceData.RACE_RESULT])
        driver_standing_qs = driver_standing_qs.annotate(c_points=Window(expression=Sum(
            'race_points'), order_by=F('race_id').asc(), partition_by=[F('driver_id')]))
        driver_standing_qs = driver_standing_qs.values_list(*columns)
        driver_standing_qs = list(driver_standing_qs)

        # Since a event can have both race and sprint we are adding them together
        driver_df = pd.DataFrame(driver_standing_qs, columns=columns)
        driver_df['c_points'] = driver_df['c_points'].replace(np.nan, 0)

        driver_df.drop_duplicates(
            ['driver_id', 'driver__name', 'race__grand_prix__abbreviation', 'race_id', 'driver__abbreviation'], keep='last')

        driver_data = []
        for driver_id, points in driver_df.groupby('driver_id')['c_points'].max().sort_values(ascending=False).items():
            driver_points_list = driver_df[driver_df['driver_id'] == driver_id][[
                'race__grand_prix__abbreviation', 'c_points']].values.tolist()
            driver_info = driver_df[driver_df['driver_id']
                                    == driver_id].iloc[0].to_dict()
            i = {
                'driverName': driver_info['driver__name'],
                'points': points,
                'pointsCumSum': driver_points_list,
            }
            driver_data.append(i)

        context_dict['driverData'] = driver_data

        engine_standing_qs = SeasonConstructorStanding.objects.filter(year=year).values(
            'engine_manufacturer', 'engine_manufacturer__name').annotate(c_points=Sum('points')).order_by('-c_points')

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
