from django.urls import path
from Circuit.views import *

urlpatterns = [
    path("<int:year>/", CircuitView.as_view(), name="circuit_year_view"),
    path("<str:circuitId>/", CircuitDetailedView.as_view(),
         name="circuit_detailed_view"),
]
