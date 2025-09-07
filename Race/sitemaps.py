from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from Race.models import Race
from django.conf import settings
from django.utils import timezone


class RaceSiteMap(Sitemap):

    def items(self):

        item_list = []

        for year in range(settings.MIN_YEAR, settings.CURRENT_YEAR+1):

            race_list = Race.objects.filter(year_id=year).only(
                "pk", "round", "date", "grand_prix__full_name")

            priority = 1 if year == settings.CURRENT_YEAR else 0.5
            change_freq = "weekly" if year == settings.CURRENT_YEAR else "never"

            item_list.append({
                "location": reverse("race_view", kwargs={"year": year}),
                "changefreq": change_freq,
                "priority": priority,
            })

            for race in race_list:

                item_list.append({
                    "location": race.race_url,
                    "lastmod": min(race.date, timezone.now().date()),
                    "priority": priority,
                })

        return item_list

    def location(self, obj):
        return obj['location']

    def priority(self, obj):
        return obj['priority']

    def changefreq(self, obj):
        return obj.get("changefreq")

    def lastmod(self, obj):
        return obj.get("lastmod")
