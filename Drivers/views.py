from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from Race.models import *
from RacePulse.utils import CREATE_REQUEST, trim_decimal_zeros


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
