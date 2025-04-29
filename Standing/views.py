from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from RacePulse.utils import CREATE_REQUEST
from Race.models import *
import pandas as pd
import copy


class CurrentStandingView(View):
    API_RESPONSE = True
    TEMPLATE = ""

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}

        year = request.TLPOST.get('year')
        columns = ['driver_id', 'driver__name', 'race_points', 'constructor_id', 'constructor__name',
                   'race__grand_prix__abbreviation', 'race_id', 'driver__abbreviation']

        driver_standing_qs = RaceData.objects.filter(
            race__year=year, type__in=[RaceData.SPRINT_RACE_RESULT, RaceData.RACE_RESULT])
        driver_standing_qs = driver_standing_qs.values_list(*columns)
        driver_standing_qs = list(driver_standing_qs)

        # Reason for computing everything in API is due to follow reason
        # -  Since a event can have both race and sprint we are adding them together
        # - We would need two queries for team and drivers
        # - max size of dataframe would be 32 * 20 = 640
        df = pd.DataFrame(driver_standing_qs, columns=columns)
        df['points'] = df['race_points'].fillna(0).astype("double")
        team_df = copy.deepcopy(df)

        df['c_points'] = df.groupby('driver_id')['points'].cumsum()
        team_df['c_points'] = team_df.groupby('constructor_id')[
            'points'].cumsum()

        df = df.drop_duplicates(['driver_id', 'driver__name', 'race__grand_prix__abbreviation',
                                'race_id', 'driver__abbreviation'], keep='last')
        team_df = team_df.drop_duplicates(
            ['constructor_id', 'constructor__name', 'race__grand_prix__abbreviation', 'race_id'], keep='last')

        driver_data = []
        for driver_id, points in df.groupby('driver_id')['c_points'].max().sort_values(ascending=False).items():
            driver_points_list = df[df['driver_id'] == driver_id][[
                'race__grand_prix__abbreviation', 'c_points']].values.tolist()
            driver_info = df[df['driver_id'] == driver_id].iloc[0].to_dict()
            i = {
                'driverName': driver_info['driver__name'],
                'points': points,
                'pointsCumSum': driver_points_list,
            }
            driver_data.append(i)

        context_dict['driverData'] = driver_data

        constructor_data = []
        for constructor_id, points in team_df.groupby('constructor_id')['c_points'].max().sort_values(ascending=False).items():
            team_points_list = team_df[team_df['constructor_id'] == constructor_id][[
                'race__grand_prix__abbreviation', 'c_points']].values.tolist()
            team_info = team_df[team_df['constructor_id']
                                == constructor_id].iloc[0].to_dict()
            i = {
                'teamName': team_info['constructor__name'],
                'points': points,
                'pointsCumSum': team_points_list,
            }
            constructor_data.append(i)

        context_dict['teamData'] = constructor_data

        if self.API_RESPONSE:
            return JsonResponse(context_dict)
