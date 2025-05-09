from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from Race.models import *
from RacePulse.utils import CREATE_REQUEST
from django.db.models.expressions import OrderBy
from django.db.models import F
from RacePulse.utils import trim_decimal_zeros


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
                "raceDate": race.event_date,
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
        year = request.TLPOST.get("year")
        race_round = request.TLPOST.get("round")

        race = Race.objects.filter(year=year, round=race_round).select_related("circuit").first()
        if not race:
            pass
            # TODO: Return 404 page

        race_data_qs = list(RaceData.objects.filter(race_id=race.pk, type=RaceData.RACE_RESULT).order_by(
            OrderBy(F("position_number"), nulls_last=True)).select_related("driver", "constructor"))

        context_dict = {
            "id": race.id,
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

        context_dict['availableData'] = race.available_events

        next_event = race.next_event
        context_dict['nextEvent'] = next_event[0]
        context_dict['nextEventType'] = next_event[1]

        race_data = []
        msg_dict = {}
        for r in race_data_qs:
            i = {
                'driver': r.driver.name,
                'position': r.position_number,
                'constructor': r.constructor.name,
                'points': trim_decimal_zeros(r.race_points),
                'startPos': r.race_grid_position_number,
                'posGain': r.race_positions_gained,
                'timeGap': r.race_gap if r.position_number else r.position_text,
            }
            if not r.position_number:
                if msg_dict.get(r.race_reason_retired):
                    msg_dict[r.race_reason_retired] += f", {r.driver.name}"
                else:
                    msg_dict[r.race_reason_retired] = f"{r.driver.name}"
            race_data.append(i)

        context_dict['raceData'] = race_data
        context_dict['active_tab'] = "Race"
        context_dict['message'] = msg_dict

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, "race/race.html", context_dict)


class RaceSessionView(View):
    SESSION_DICT = {'FP1': RaceData.FREE_PRACTICE_1_RESULT,
                    'FP2': RaceData.FREE_PRACTICE_2_RESULT,
                    'FP3': RaceData.FREE_PRACTICE_3_RESULT,
                    'Sprint Qualifying': RaceData.SPRINT_QUALIFYING_RESULT,
                    'Qualifying': RaceData.QUALIFYING_RESULT,
                    'Sprint': RaceData.SPRINT_RACE_RESULT,
                    'Race': RaceData.RACE_RESULT,
                    }
    FREE_PRACTICE_TEMPLATE = "race/_partials/practice.html"
    QUALI_TEMPLATE = "race/_partials/qualifying.html"
    RACE_TEMPLATE = "race/_partials/race.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        template = ""

        race_id = request.TLPOST.get('race_id')
        session = request.TLPOST.get("session")

        race_data_qs = list(RaceData.objects.filter(race_id=race_id, type=self.SESSION_DICT.get(session)).order_by(
            OrderBy(F("position_number"), nulls_last=True)).select_related("driver", "constructor"))

        race_data = []
        msg_dict = {}

        if session in ['Race', 'Sprint']:
            template = self.RACE_TEMPLATE
            for r in race_data_qs:
                i = {
                    'driver': r.driver.name,
                    'position': r.position_number,
                    'constructor': r.constructor.name,
                    'points': trim_decimal_zeros(r.race_points),
                    'startPos': r.race_grid_position_number,
                    'posGain': r.race_positions_gained,
                    'timeGap': r.race_gap if r.position_number else r.position_text,

                }
                race_data.append(i)
                if not r.position_number:
                    if msg_dict.get(r.race_reason_retired):
                        msg_dict[r.race_reason_retired] += f", {r.driver.name}"
                    else:
                        msg_dict[r.race_reason_retired] = f"{r.driver.name}"

        if session in ['Qualifying', 'Sprint Qualifying']:
            template = self.QUALI_TEMPLATE
            for r in race_data_qs:
                i = {
                    'driver': r.driver.name,
                    'position': r.position_number,
                    'constructor': r.constructor.name,
                    'q1': r.qualifying_q1,
                    'q2': r.qualifying_q2,
                    'q3': r.qualifying_q3,
                    'timeGap': r.qualifying_gap,
                }
                race_data.append(i)

        if session in ['FP1', 'FP2', 'FP3']:
            template = self.FREE_PRACTICE_TEMPLATE
            for r in race_data_qs:
                i = {
                    'driver': r.driver.name,
                    'position': r.position_number,
                    'constructor': r.constructor.name,
                    'time': r.practice_time,
                    'timeGap': r.practice_gap,

                }
                race_data.append(i)

        context_dict = {}
        context_dict['raceData'] = race_data
        context_dict['message'] = msg_dict

        return render(request, template, context_dict)
