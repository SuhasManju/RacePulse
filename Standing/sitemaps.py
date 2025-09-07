from django.contrib.sitemaps import Sitemap
from django.conf import settings
from django.urls import reverse


class StandingSiteMap(Sitemap):

    def items(self):
        return list(range(settings.MIN_YEAR, settings.CURRENT_YEAR+1))

    def location(self, obj):
        return reverse("standing", kwargs={"year": obj})

    def priority(self, obj):
        if obj == settings.CURRENT_YEAR:
            return 1
        return 0.5
