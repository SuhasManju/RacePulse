from django.shortcuts import render
from django.views import View
from Race.models import *
from RacePulse.utils import CREATE_REQUEST, trim_decimal_zeros
from django.db.models import Q, Count, Min
from django.http.response import JsonResponse
from django.conf import settings
from django.db.models import Subquery
from collections import defaultdict

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
            "bestChampionPos": team.best_championship_position,
            "highestRaceFinish": team.best_race_result,
            "highestRaceStart": team.best_starting_grid_position,
            "teamImg": team.team_img,
            "teamSmImg": team.team_sm_img,
            "teamColor": team.team_color,
        }

        context_dict['teamData'] = team_data

        latest_race_pk = RaceData.objects.filter(constructor_id=team_id).order_by(
            '-race_id').values_list('race_id')[:1]

        current_drivers = RaceData.objects.filter(
            race_id=Subquery(latest_race_pk), type=RaceData.RACE_RESULT, constructor_id=team_id).select_related("driver")

        driver_data = []
        for d in current_drivers:
            temp = {
                "driverId": d.driver_id,
                "driverName": d.driver.name,
                "driverImg": d.driver.driver_img,
                "driverNo": d.driver_number if d.driver_number else d.driver.permanent_number,
            }
            driver_data.append(temp)

        context_dict['driverData'] = driver_data

        previous_year_list = []
        previous_year_standing_qs = SeasonConstructorStanding.objects.filter(
            constructor_id=team_id).order_by("year")

        for i in previous_year_standing_qs:
            temp = {
                "year": i.year_id,
                "position": i.position_number,
                "points": i.points,
            }
            previous_year_list.append(temp)

        context_dict['previousYearData'] = previous_year_list

        team_cronology_qs = ConstructorChronology.objects.filter(constructor_id=team_id).order_by(
            "-year_from").select_related("other_constructor")
        team_cronology_list = []

        for team in team_cronology_qs:
            temp = {
                "constructorId": team.other_constructor_id,
                "constructor": team.other_constructor.name,
                "yearFrom": team.year_from,
                "yearTo": team.year_to,
            }
            team_cronology_list.append(temp)
        context_dict['cronologyData'] = team_cronology_list

        race_annotate_dict = {
            "total_wins": Count("position_number", filter=Q(position_number=1)),
            "total_podiums": Count("position_number", filter=Q(position_number__gte=1, position_number__lte=3)),
            "best_result": Min("position_number"),
        }
        quali_annotate_dict = {
            "total_poles": Count("position_number", filter=Q(position_number=1)),
            "best_quali_pos": Min("position_number"),
        }

        team_driver_qs = SeasonEntrantDriver.objects.filter(
            constructor_id=team_id, test_driver=False).select_related("driver").order_by("-year")
        team_driver_race_qs = RaceData.objects.filter(
            type__in=[RaceData.RACE_RESULT], constructor_id=team_id).values("driver_id").annotate(**race_annotate_dict)
        team_driver_quali_qs = RaceData.objects.filter(
            type__in=[RaceData.QUALIFYING_RESULT], constructor_id=team_id).values("driver_id").annotate(**quali_annotate_dict)
        team_driver_list = []
        team_driver_year = defaultdict(list)
        team_driver_rounds = defaultdict(int)
        team_driver_dict = defaultdict()
        team_driver_race_dict = {
            driver['driver_id']: driver for driver in team_driver_race_qs}
        team_driver_quali_dict = {
            driver['driver_id']: driver for driver in team_driver_quali_qs}

        for team_driver in team_driver_qs:
            team_driver_year[team_driver.driver_id].append(
                str(team_driver.year_id))
            team_driver_rounds[team_driver.driver_id] += len(
                team_driver.rounds.split(";"))
            team_driver_dict[team_driver.driver_id] = team_driver.driver.name

        for driver in team_driver_dict.keys():
            driver_race_dict = team_driver_race_dict[driver]
            driver_quali_dict = team_driver_quali_dict[driver]
            temp = {
                "driverId": driver,
                "name": team_driver_dict[driver],
                "years": ", ".join(team_driver_year[driver]),
                "noRounds": team_driver_rounds[driver],
                "noWins": driver_race_dict['total_wins'],
                "totalPodiums": driver_race_dict['total_podiums'],
                "bestResult": driver_race_dict['best_result'],
                "noPoles": driver_quali_dict['total_poles'],
                "bestQualiPos": driver_quali_dict['best_quali_pos'],
            }
            team_driver_list.append(temp)

        context_dict["previousDriverData"] = team_driver_list


        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, self.template, context_dict)
