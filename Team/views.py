from django.shortcuts import render
from django.views import View
from Race.models import *
from RacePulse.utils import CREATE_REQUEST
from django.http.response import JsonResponse


class TeamView(View):
    API_RESPONSE = True

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        year = request.TLPOST.get('year')
        team_qs = SeasonConstructorStanding.objects.filter(
            year=year).order_by("-points")

        team_data = []
        for t in team_qs:
            team_data.append(
                {
                    'id': t.constructor.pk,
                    "name": t.constructor.name,
                    "points": t.points,
                    "teamImg": t.constructor.team_sm_img,
                }
            )

        context_dict['teamData'] = team_data

        return JsonResponse(context_dict)
