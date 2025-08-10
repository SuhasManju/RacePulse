from django.shortcuts import render
from django.views import View
from RacePulse.utils import CREATE_REQUEST, retrive_driver_list, retrive_team_list
from Comparision.compare_entity import CompareDriver, CompareTeam


class DriverComparisionView(View):
    TEMPLATE = "comparisions/driver_comp.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        self.make_context_dict()

        return render(request, self.TEMPLATE, self.context_dict)

    def make_context_dict(self):
        self.context_dict = {
            "driverList": retrive_driver_list(self.request.year)}

        driver1Id = self.request.TLPOST.get("driver1Id")
        driver2Id = self.request.TLPOST.get("driver2Id")

        if driver1Id and driver2Id:
            driver_list = [driver1Id, driver2Id]

            obj = CompareDriver(driver_list, self.request.year)
            result = obj.make_context_dict()

            self.context_dict['driver1Data'] = result.get(driver1Id)
            self.context_dict['driver2Data'] = result.get(driver2Id)

            self.context_dict['driver1Name'] = driver1Id.replace(
                "-", " ").title()
            self.context_dict['driver2Name'] = driver2Id.replace(
                "-", " ").title()


class TeamComparisionView(View):
    TEMPLATE = "comparisions/team_comp.html"

    @CREATE_REQUEST
    def get(self, request, *args, **kwargs):
        self.make_context_dict()

        return render(request, self.TEMPLATE, self.context_dict)

    def make_context_dict(self):
        self.context_dict = {"teamList": retrive_team_list(self.request.year)}

        team1Id = self.request.TLPOST.get('team1Id')
        team2Id = self.request.TLPOST.get('team2Id')

        if team1Id and team2Id:
            team_list = [team1Id, team2Id]

            obj = CompareTeam(team_list, self.request.year)
            result = obj.make_context_dict()

            self.context_dict['team1Data'] = result.get(team1Id)
            self.context_dict['team2Data'] = result.get(team2Id)

            self.context_dict['team1Name'] = team1Id.replace("-", ' ').title()
            self.context_dict['team2Name'] = team2Id.replace("-", ' ').title()
