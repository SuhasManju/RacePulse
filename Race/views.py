from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from Race.models import *
from RacePulse.utils import CREATE_REQUEST


class RaceView(View):
    API_RESPONSE = False

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {"head": {"status": "0", "statusDescription": ""}}
        table_data = []
        year = request.TLPOST.get("year")
        races = list(Race.objects.filter(year=year).order_by("round"))

        if not races:
            context_dict["head"]["status"] = "2"
            context_dict["head"]["statusDescription"] = "No races found"
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
        context_dict["body"] = table_data
        if self.API_RESPONSE:
            return JsonResponse(table_data)

        return render(self.request, "race/index.html", context_dict)


class RaceDetailedView(View):
    API_RESPONSE = False

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {"head": {"status": "0", "statusDescription": ""}}

        year = request.TLPOST.get("year")
        race_round = request.TLPOST.get("round")

        race = Race.objects.filter(year=year, round=race_round).first()
        if not race:
            context_dict["head"]["status"] = "2"
            context_dict["head"]["statusDescription"] = "No race found"
            # TODO: Return 404 page

        table_data = {
            "officalName": race.official_name,
            "isSprint": race.is_sprint,
            "fp1Time": race.fp1_time,
            "fp2Time": race.fp2_time,
            "fp3Time": race.fp3_time,
            "qualiTime": race.quali_time,
            "sprintQualiTime": race.fp1_time,
            "raceTime": race.race_time,
        }
        context_dict["body"] = table_data

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, "race/race.html", context_dict)
