from django.urls import path
from Comparision.views import *

urlpatterns = [
    path("driver/<int:year>/", DriverComparisionView.as_view(),
         name="DriverComparision"),
    path("driver/<int:year>/<str:driver1Id>-vs-<str:driver2Id>/", DriverComparisionView.as_view(),
         name="DriverComparision"),
    path("team/<int:year>/", TeamComparisionView.as_view(),
         name="TeamComparision"),
    path("team/<int:year>/<str:team1Id>-vs-<str:team2Id>/", TeamComparisionView.as_view(),
         name="DriverComparision"),
]
