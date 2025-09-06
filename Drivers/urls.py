from django.urls import path
from Drivers.views import *

urlpatterns = [
    path("<int:year>/", DriverView.as_view(), name="drivers_home_page"),
    path("<str:driverId>/", DriverDetailedView.as_view(),
         name="drivers_detailed_view"),
]
