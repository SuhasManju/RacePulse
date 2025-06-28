from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q, F, OrderBy
from django.utils import timezone
from django.conf import settings
from RacePulse.utils import CREATE_REQUEST
from Race.models import Driver, Constructor, Circuit, Race, RaceData, SeasonDriverStanding, SeasonConstructorStanding
from RacePulse.utils import trim_decimal_zeros

class SearchView(APIView):

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        search_item = request.TLPOST.get("search")
        if not search_item:
            return Response(context_dict)

        driver_list = []
        driver_qs = Q(full_name__icontains=search_item)
        driver_qs |= Q(permanent_number=search_item)
        driver_qs |= Q(abbreviation__icontains=search_item)
        drivers = Driver.objects.filter(driver_qs)[:6]

        for driver in drivers:
            temp = {
                "name": driver.name,
                "link": driver.driver_url,
            }
            driver_list.append(temp)
        context_dict['drivers'] = driver_list

        team_list = []
        team_qs = Q(full_name__icontains=search_item)
        teams = Constructor.objects.filter(team_qs)[:6]

        for team in teams:
            temp = {
                "name": team.name,
                "link": team.team_url,
            }
            team_list.append(temp)
        context_dict['teams'] = team_list

        circuit_list = []
        circuit_qs = Q(full_name__icontains=search_item)
        circuit_qs |= Q(previous_names__icontains=search_item)
        circuit_qs |= Q(country__name__icontains=search_item)
        circuits = Circuit.objects.filter(circuit_qs)[:6]

        for circuit in circuits:
            temp = {
                "name": circuit.name,
                "link": circuit.circuit_url,
            }
            circuit_list.append(temp)
        context_dict["circuits"] = circuit_list

        return Response(context_dict)


class HomeView(View):
    API_RESPONSE = False
    TEMPLATE = "index.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        year = request.TLPOST.get("year", settings.CURRENT_YEAR)

        current_time = timezone.now()
        latest_race_pk = RaceData.objects.order_by(
            '-race_id').values_list('race_id', flat=True).first()

        driver_standing_qs = SeasonDriverStanding.objects.filter(
            year_id=year).order_by("position_number").select_related("driver")
        team_standing_qs = SeasonConstructorStanding.objects.filter(
            year_id=year).order_by("position_number").select_related("constructor")

        race_qs = Race.objects.filter(
            year_id=year).select_related("circuit").order_by("pk")


        last_race_result = []
        if year == settings.CURRENT_YEAR:
            latest_result_qs = RaceData.objects.filter(race_id=latest_race_pk,
                                                       type=RaceData.RACE_RESULT).order_by(
                OrderBy(F("position_number"), nulls_last=True)).values_list(
                    "position_number", "driver__name", "constructor__name", "race_gap")[:3]
            for position, driver_name, team_name, race_gap in latest_result_qs:
                temp = {
                    "position": position,
                    "driverName": driver_name,
                    "teamName": team_name,
                    "gap": race_gap,
                }
                last_race_result.append(temp)

        races_list = []
        next_race = {}
        last_race = {}
        for race in race_qs:
            temp = {
                "round": race.round,
                "name": race.official_name,
                "co_ordinates": race.circuit.cor_ordinates,
                "date": race.event_date,
            }

            if not next_race and race.race_time > current_time:
                next_race = {
                    "name": race.official_name,
                    "nextEvent": race.next_event[0],
                    "nextEventType": race.next_event[1],
                    "round": race.round,
                    "year": race.year_id,
                }

            if latest_race_pk == race.pk:
                last_race = {
                    "round": race.round,
                    "year": race.year_id,
                    "name": race.official_name,
                }

            races_list.append(temp)
        context_dict['raceData'] = races_list
        context_dict['nextRace'] = next_race

        if last_race_result:
            last_race['standings'] = last_race_result

        context_dict['lastRaceResult'] = last_race

        driver_standing_list = []
        for standing in driver_standing_qs:
            temp = {
                "pk": standing.driver.pk,
                "name": standing.driver.name,
                "img": standing.driver.driver_img,
                "points": trim_decimal_zeros(standing.points),
            }
            driver_standing_list.append(temp)
        context_dict['driverStanding'] = driver_standing_list

        team_standing_list = []
        for standing in team_standing_qs:
            temp = {
                "pk": standing.constructor.pk,
                "name": standing.constructor.name,
                "img": standing.constructor.team_sm_img,
                "points": trim_decimal_zeros(standing.points),
            }
            team_standing_list.append(temp)
        context_dict['teamStanding'] = team_standing_list

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, self.TEMPLATE, context_dict)
