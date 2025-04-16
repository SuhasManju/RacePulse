from Race.views import *
from django.urls import path
from .views import *

urlpatterns = [
    path("<int:year>/", RaceView.as_view(), name="race"),
    path("<int:year>/<int:round>/", RaceDetailedView.as_view(), name="race_result"),
]
