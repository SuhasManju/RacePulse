from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap, index
from RacePulse.views import SearchView, HomeView
from django.views.generic import TemplateView

from Team.sitemaps import TeamSiteMap
from Drivers.sitemaps import DriverSiteMap
from Circuit.sitemaps import CircuitSiteMap
from Standing.sitemaps import StandingSiteMap
from Comparision.sitemaps import ComparisionSiteMap
from Race.sitemaps import RaceSiteMap


sitemaps = {
    "teams": TeamSiteMap,
    "drivers": DriverSiteMap,
    "circuits": CircuitSiteMap,
    "standings": StandingSiteMap,
    "comparisons": ComparisionSiteMap,
    "races": RaceSiteMap,
}

urlpatterns = [
    path("e@am!nat!0n/", admin.site.urls),
    path("race/", include("Race.urls")),
    path("standing/", include("Standing.urls")),
    path("team/", include("Team.urls")),
    path("drivers/", include("Drivers.urls")),
    path("circuits/", include("Circuit.urls")),
    path("comparision/", include("Comparision.urls")),
    path("search/", SearchView.as_view(), name="webSearch"),
    path("", HomeView.as_view(), name="home"),
    path("<int:year>/", HomeView.as_view(), name="home"),
    path("__reload__/", include("django_browser_reload.urls")),

    # SiteMap Urls
    path('sitemap.xml', index, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.index'),
    path('sitemap-<section>.xml', sitemap,
         {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(
        template_name="robots.txt", content_type="text/plain")),
]
