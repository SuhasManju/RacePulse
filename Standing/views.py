from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from RacePulse.utils import CREATE_REQUEST, CREATE_REQUEST_POST
from Race.models import *
import pandas as pd
from RacePulse.utils import TEAM_COLOR_DICT, smart_format, random_colours
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random

@method_decorator(csrf_exempt, name='dispatch')
class CurrentStandingView(View):
    API_RESPONSE = False
    TEMPLATE = "standings/standings.html"

    def dispatch(self, request, *args, **kwargs):
        self.context_dict = {}
        self.columns = ['driver_id', 'driver__name', 'race_points', 'constructor_id', 'constructor__name',
                        'race__grand_prix__abbreviation', 'race_id', 'driver__abbreviation']
        return super().dispatch(request, *args, **kwargs)

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        self.parse_input()
        self.make_qs()
        self.make_driver_context_dict()
        self.make_team_context_dict()

        if self.API_RESPONSE:
            return JsonResponse(self.context_dict)

        return render(request, self.TEMPLATE, self.context_dict)

    @CREATE_REQUEST_POST
    def post(self, request, *args, **kwargs):
        self.parse_input()
        self.make_qs()
        if self.driver_ids:
            self.make_driver_context_dict()
        if self.team_ids:
            self.make_team_context_dict()
        if not self.driver_ids and not self.team_ids:
            self.make_driver_context_dict()
            self.make_team_context_dict()
        return JsonResponse(self.context_dict)

    def parse_input(self):
        self.year = self.request.TLPOST.get("year")
        self.driver_ids = self.request.TLPOST.get("driverList")
        self.team_ids = self.request.TLPOST.get("teamList")

    def make_qs(self):
        q = Q(type__in=[RaceData.SPRINT_RACE_RESULT, RaceData.RACE_RESULT])
        q &= Q(race__year=self.year)

        if self.driver_ids:
            q &= Q(driver_id__in=self.driver_ids)

        if self.team_ids:
            q &= Q(constructor_id__in=self.team_ids)

        driver_standing_qs = RaceData.objects.filter(q)
        driver_standing_qs = driver_standing_qs.values_list(*self.columns)
        self.driver_standing_qs = list(driver_standing_qs)

    # Reason for computing everything in API is due to follow reason
    # -  Since a event can have both race and sprint we are adding them together
    # - We would need two queries for team and drivers
    # - max size of dataframe would be 32 * 20 = 640

    def make_driver_context_dict(self):
        df = pd.DataFrame(self.driver_standing_qs, columns=self.columns)
        df['points'] = df['race_points'].fillna(0).astype("double")
        df['c_points'] = df.groupby('driver_id')['points'].cumsum()
        df = df.drop_duplicates(['driver_id', 'driver__name', 'race__grand_prix__abbreviation',
                                'race_id', 'driver__abbreviation'], keep='last')

        driver_data = []
        already_visited_team = set()
        for driver_id, points in df.groupby('driver_id')['c_points'].max().sort_values(ascending=False).items():
            driver_points_list = df[df['driver_id'] == driver_id][[
                'race__grand_prix__abbreviation', 'c_points']].values.tolist()
            driver_info = df[df['driver_id'] == driver_id].iloc[0].to_dict()

            driver_color = TEAM_COLOR_DICT.get(
                driver_info['constructor_id']) or random.choice(random_colours)

            if driver_info['constructor_id'] in already_visited_team:
                driver_color = invert_hex_color(driver_color)
            already_visited_team.add(driver_info['constructor_id'])

            i = {
                'driverId': driver_id,
                'driverName': driver_info['driver__name'],
                'points': smart_format(points),
                'pointsCumSum': driver_points_list,
                'color': driver_color
            }
            driver_data.append(i)

        self.context_dict['driverData'] = driver_data

    def make_team_context_dict(self):
        team_df = pd.DataFrame(self.driver_standing_qs, columns=self.columns)
        team_df['points'] = team_df['race_points'].fillna(0).astype("double")
        team_df['c_points'] = team_df.groupby('constructor_id')[
            'points'].cumsum()
        team_df = team_df.drop_duplicates(
            ['constructor_id', 'constructor__name', 'race__grand_prix__abbreviation', 'race_id'], keep='last')

        constructor_data = []
        for constructor_id, points in team_df.groupby('constructor_id')['c_points'].max().sort_values(ascending=False).items():
            team_points_list = team_df[team_df['constructor_id'] == constructor_id][[
                'race__grand_prix__abbreviation', 'c_points']].values.tolist()
            team_info = team_df[team_df['constructor_id']
                                == constructor_id].iloc[0].to_dict()
            i = {
                'teamId': constructor_id,
                'teamName': team_info['constructor__name'],
                'points': smart_format(points),
                'pointsCumSum': team_points_list,
                'color': TEAM_COLOR_DICT.get(constructor_id)
            }
            constructor_data.append(i)

        self.context_dict['teamData'] = constructor_data

        self.context_dict['labels'] = team_df['race__grand_prix__abbreviation'].unique(
        ).tolist()
