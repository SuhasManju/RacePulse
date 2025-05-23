from Race.views import *
from django.urls import path

urlpatterns = [
    path("<int:year>/", RaceView.as_view(), name="race"),
    path("<int:year>/<int:round>/", RaceDetailedView.as_view(), name="race_result"),
    path("session/<int:race_id>/", RaceSessionView.as_view(), name="session_data")
]
