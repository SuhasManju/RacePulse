from django.urls import path
from Team.views import *


urlpatterns = [
    path("<int:year>/", TeamView.as_view(), name="Race"),
]
