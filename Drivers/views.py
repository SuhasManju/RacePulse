from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from Race.models import *
from RacePulse.utils import CREATE_REQUEST, trim_decimal_zeros
from dateutil.relativedelta import relativedelta


class DriverView(View):
    API_RESPONSE = False
    TEMPLATE = "drivers/index.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        year = request.TLPOST.get("year")

        driver_list = []
        driver_list_qs = SeasonDriverStanding.objects.filter(
            year_id=year).order_by("position_number").select_related("driver")
        for driver in driver_list_qs:
            temp = {
                "id": driver.driver_id,
                "name": driver.driver.name,
                "points": trim_decimal_zeros(driver.points),
            }
            driver_list.append(temp)

        context_dict['driverData'] = driver_list

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, self.TEMPLATE, context_dict)


class DriverDetailedView(View):
    API_RESPONSE = False
    TEMPLATE = "drivers/drivers.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {}
        driver_id = request.TLPOST.get("driverId")

        driver = Driver.objects.select_related(
            "country_of_birth_country", "nationality_country").get(pk=driver_id)
        current_team = RaceData.objects.filter(
            driver_id=driver_id).order_by("-race_id").select_related("constructor").first()
        today = datetime.now()
        age_diff = relativedelta(today, driver.date_of_birth)

        driver_data = {
            "id": driver_id,
            "name": driver.name,
            "fullName": driver.full_name,
            "dob": driver.date_of_birth,
            "age": f"{age_diff.years} Years and {age_diff.months} Months",
            "birthPlace": driver.place_of_birth + ", " + driver.country_of_birth_country.name,
            "nationality": driver.nationality_country.name,
            "noOfChampionShip": driver.total_championship_wins,
            "noOfWins": driver.total_race_wins,
            "noOfPoles": driver.total_pole_positions,
            "highestChampionshipPos": driver.best_championship_position,
            "highestPosFinish": driver.best_race_result,
            "highestPosStart": driver.best_starting_grid_position,
            "driverNumber": driver.permanent_number,
            "noOfPodiums": driver.total_podiums,
            "currentTeam": current_team.constructor.name,
            "noOfRaces": driver.total_race_starts,
            "driverImg": driver.driver_img,
        }
        context_dict['driverData'] = driver_data

        if self.API_RESPONSE:
            return JsonResponse(context_dict)

        return render(request, self.TEMPLATE, context_dict)
