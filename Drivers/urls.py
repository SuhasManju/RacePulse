from django.urls import path
from Drivers.views import *

urlpatterns = [
    path("<int:year>/", DriverView.as_view(), name="drivers"),
    path("<str:driverId>/", DriverDetailedView.as_view(),
         name="drivers_detailed_view"),
]
