from django.shortcuts import render
from django.views import View
from RacePulse.utils import CREATE_REQUEST
from RacePulse.utils import retrive_driver_list, retrive_team_list


class DriverComparisionView(View):
    TEMPLATE = "comparisions/driver_comp.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {"driverList": retrive_driver_list(request.year)}

        return render(request, self.TEMPLATE, context_dict)


class TeamComparisionView(View):
    TEMPLATE = "comparisions/team_comp.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        context_dict = {"teamList": retrive_team_list(request.year)}

        return render(request, self.TEMPLATE, context_dict)
