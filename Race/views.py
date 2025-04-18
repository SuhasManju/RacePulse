from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from Race.models import *
from RacePulse.utils import CREATE_REQUEST


class RaceView(View):
    API_RESPONSE = False

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        table_data = []
        year = request.TLPOST.get("year")
        races = list(Race.objects.filter(year=year).order_by("round"))

        if not races:
            pass
            # TODO: Return 404 page

        for race in races:
            res = {
                "id": race.id,
                "fullName": race.official_name,
                "raceNo": race.round,
                "raceDate": race.date,
                "isSprint": race.is_sprint,
            }
            table_data.append(res)
        context_dict["races"] = table_data
        if self.API_RESPONSE:
            return JsonResponse(table_data)

        return render(self.request, "race/index.html", context_dict)


class RaceDetailedView(View):
    API_RESPONSE = False

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        available_data = []

        year = request.TLPOST.get("year")
        race_round = request.TLPOST.get("round")

        race = Race.objects.filter(year=year, round=race_round).select_related("circuit").first()
        if not race:
            pass
            # TODO: Return 404 page
 
        context_dict = {
            "officalName": race.official_name,
            "name": race.grand_prix.full_name,
            "isSprint": race.is_sprint,
            "fp1Time": race.fp1_time,
            "fp2Time": race.fp2_time,
            "fp3Time": race.fp3_time,
            "qualiTime": race.quali_time,
            "sprintQualiTime": race.sprint_quali_time,
            "sprintTime": race.sprint_time,
            "raceTime": race.race_time,
            "circuitImg": race.circuit.circuit_image,
            "noLaps": race.laps,
            "totalDist": race.distance,
            "length": race.course_length,
        }

        data_map = [
            (race.fp1_time, "FP1"),
            (race.sprint_quali_time, "Sprint Qualifying"),
            (race.fp2_time, "FP2"),
            (race.fp3_time, "FP3"),
            (race.quali_time, "Qualifying"),
            (race.sprint_time, "Sprint"),
        ]

        available_data = [label for time, label in data_map if time]
        available_data.append("Race")

        context_dict['availableData'] = available_data


        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, "race/race.html", context_dict)
