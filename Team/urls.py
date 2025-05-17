from django.urls import path
from Team.views import *


urlpatterns = [
    path("<int:year>/", TeamView.as_view(), name="team_home_page"),
    path("<str:teamId>/", TeamDetailedView.as_view(), name="team_page"),
]
