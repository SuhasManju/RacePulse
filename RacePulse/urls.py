from django.contrib import admin
from django.urls import path, include
from RacePulse.views import SearchView

urlpatterns = [
    path("e@am!nat!0n/", admin.site.urls),
    path("race/", include("Race.urls")),
    path("standing/", include("Standing.urls")),
    path("team/", include("Team.urls")),
    path("drivers/", include("Drivers.urls")),
    path("circuits/", include("Circuit.urls")),
    path("search/", SearchView.as_view(), name="webSearch"),
    path("__reload__/", include("django_browser_reload.urls")),
]
