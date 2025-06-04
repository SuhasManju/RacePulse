from django.shortcuts import render
from Race.models import *
from django.views import View
from django.http import JsonResponse
from RacePulse.utils import CREATE_REQUEST


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

        return render(request, self.TEMPLATE, context_dict)
