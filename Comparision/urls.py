from django.urls import path
from Comparision.views import *

urlpatterns = [
    path("driver/<int:year>/", DriverComparisionView.as_view(),
         name="DriverComparision"),
    path("team/<int:year>/", TeamComparisionView.as_view(),
         name="TeamComparisionView"),
]
