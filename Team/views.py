from django.shortcuts import render
from django.views import View
from Race.models import *
from RacePulse.utils import CREATE_REQUEST, trim_decimal_zeros, retrive_latest_race_pk
from django.http.response import JsonResponse
from django.conf import settings

class TeamView(View):
    API_RESPONSE = False
    template = "teams/index.html"

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
                    "points": trim_decimal_zeros(t.points),
                    "teamImg": t.constructor.team_sm_img,
                }
            )

        context_dict['teamData'] = team_data

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, self.template, context_dict)


class TeamDetailedView(View):
    API_RESPONSE = False
    template = "teams/teams.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        team_id = request.TLPOST.get("teamId")

        team = Constructor.objects.select_related("country").get(pk=team_id)
        season_data = SeasonEntrantChassis.objects.filter(
            constructor_id=team_id).select_related("engine_manufacturer", "chassis").last()

        latest_race_pk = retrive_latest_race_pk()

        team_data = {
            "id": team_id,
            "name": team.name,
            "fullName": team.full_name,
            "country": team.country.name,
            "engineSupplier": season_data.engine_manufacturer.name,
            "chassisNo": season_data.chassis.name,
            "totalChampionShip": team.total_championship_wins,
            "carImg": season_data.car_image,
            "highestChampionShip": team.best_championship_position,
            "polePositions": team.total_pole_positions,
            "raceWins": team.total_race_wins,
            "totalPodiums": team.total_podiums,
            "teamImg": team.team_img,
            "teamSmImg": team.team_sm_img,
            "teamColor": team.team_color,
        }

        context_dict['teamData'] = team_data

        current_drivers = RaceData.objects.filter(
            race_id=latest_race_pk, type=RaceData.RACE_RESULT, constructor_id=team_id).select_related("driver")

        driver_data = []
        for d in current_drivers:
            temp = {
                "driverId": d.driver_id,
                "driverName": d.driver.name,
                "driverImg": d.driver.driver_img,
                "driverNo": d.driver.permanent_number,
            }
            driver_data.append(temp)

        context_dict['driverData'] = driver_data

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        print(context_dict)
        return render(request, self.template, context_dict)
