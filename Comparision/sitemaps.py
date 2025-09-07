from django.contrib.sitemaps import Sitemap
from django.conf import settings
from Race.models import SeasonDriverStanding, SeasonConstructorStanding
from itertools import combinations
from django.urls import reverse


class ComparisionSiteMap(Sitemap):

    def items(self):

        item_list = []

        for year in range(settings.MIN_YEAR, settings.CURRENT_YEAR+1):
            priority = 1 if year == settings.CURRENT_YEAR else 0.5
            change_freq = "weekly" if year == settings.CURRENT_YEAR else "never"

            driver_pks = SeasonDriverStanding.objects.filter(
                year_id=year).values_list("driver_id", flat=True)

            driver_combinations = list(combinations(driver_pks, 2))

            item_list.append({
                "location": reverse("DriverComparisionHomePage", kwargs={"year": year}),
                "changefreq": change_freq,
                "priority": priority,
            })

            for driver1, driver2 in driver_combinations:
                item_list.append({
                    "location": reverse("DriverComparision", kwargs={"year": year, "driver1Id": driver1, "driver2Id": driver2}),
                    "changefreq": change_freq,
                    "priority": priority
                })

            team_pks = SeasonConstructorStanding.objects.filter(
                year_id=year).values_list("constructor_id", flat=True)

            team_combinations = list(combinations(team_pks, 2))

            item_list.append({
                "location": reverse("TeamComparisionHomePage", kwargs={"year": year}),
                "changefreq": change_freq,
                "priority": priority,
            })

            for team1, team2 in team_combinations:
                item_list.append({
                    "location": reverse("TeamComparision", kwargs={"year": year, "team1Id": team1, "team2Id": team2}),
                    "changefreq": change_freq,
                    "priority": priority
                })

        return item_list

    def location(self, obj):
        return obj['location']

    def changefreq(self, obj):
        return obj['changefreq']

    def priority(self, obj):
        return obj['priority']
