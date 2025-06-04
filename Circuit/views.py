from django.shortcuts import render
from Race.models import *
from django.views import View
from django.http import JsonResponse
from RacePulse.utils import CREATE_REQUEST
from collections import defaultdict


class CircuitView(View):
    API_RESPONSE = False
    TEMPLATE = "circuits/index.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        year = request.TLPOST.get("year")

        circuit_qs = Race.objects.filter(year_id=year).select_related(
            "circuit", "circuit__country")
        circuit_list = []

        for c in circuit_qs:
            temp = {
                "circuitId": c.circuit_id,
                "name": c.circuit.full_name,
                "place": c.circuit.place_name + ", " + c.circuit.country.name,
            }
            circuit_list.append(temp)

        context_dict['circuitData'] = circuit_list

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, self.TEMPLATE, context_dict)


class CircuitDetailedView(View):
    API_RESPONSE = False
    TEMPLATE = "circuits/circuit.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        circuit_id = request.TLPOST.get("circuitId")

        circuit = Circuit.objects.select_related("country").get(pk=circuit_id)
        circuit_data = {
            "id": circuit_id,
            "name": circuit.name,
            "fullName": circuit.full_name,
            "place": circuit.place_name + ", " + circuit.country.name,
            "coOrdinates": circuit.cor_ordinates,
            "totalRacesHeld": circuit.total_races_held,
            "circuitImg": circuit.circuit_image,
        }
        context_dict['circuitData'] = circuit_data

        previous_year_qs = RaceData.objects.filter(type__in=[RaceData.RACE_RESULT],
                                                   race__circuit_id=circuit_id, position_number=1)
        previous_year_qs = previous_year_qs.select_related(
            "constructor", "driver", "race")
        previous_year_qs = previous_year_qs.order_by("-race__year_id")
        previous_year_list = []
        max_wins_drivers_dict = defaultdict(int)
        max_wins_teams_dict = defaultdict(int)

        for race_data in previous_year_qs:
            temp = {
                "raceId": race_data.race_id,
                "year": race_data.race.year_id,
                "round": race_data.race.round,
                "driver": race_data.driver.name,
                "driverId": race_data.driver_id,
                "team": race_data.constructor.name,
                "teamId": race_data.constructor_id,
            }
            max_wins_drivers_dict[race_data.driver.name] += 1
            max_wins_teams_dict[race_data.constructor.name] += 1

            previous_year_list.append(temp)

        max_win_driver, max_win_driver_count = max(
            max_wins_drivers_dict.items(), key=lambda x: x[1])
        max_win_team, max_win_team_count = max(
            max_wins_teams_dict.items(), key=lambda x: x[1])

        circuit_data['maxWinDriver'] = max_win_driver
        circuit_data['maxWinDriverCount'] = max_win_driver_count
        circuit_data['maxWinTeam'] = max_win_team
        circuit_data['maxWinTeamCount'] = max_win_team_count

        context_dict['previousYearData'] = previous_year_list

        return render(request, self.TEMPLATE, context_dict)
