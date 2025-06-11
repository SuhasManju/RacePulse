from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from RacePulse.utils import CREATE_REQUEST
from Race.models import Driver, Constructor, Circuit


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
