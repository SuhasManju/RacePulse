from django.contrib.sitemaps import Sitemap
from Race.models import Circuit, Race
from django.urls import reverse
from django.conf import settings


class CircuitSiteMap(Sitemap):

    def __init__(self):
        super().__init__()
        self.current_year_circuits = Race.objects.filter(
            year_id=settings.CURRENT_YEAR).values_list("circuit_id", flat=True)

    def items(self):
        drivers = Circuit.objects.all().only("pk")
        years = range(settings.MIN_YEAR, settings.CURRENT_YEAR + 1)

        # Combine both constructors and years into one iterable
        return list(drivers) + list(years)

    def location(self, item):
        if isinstance(item, Circuit):
            return reverse("circuit_detailed_view", kwargs={"circuitId": item.pk})
        elif isinstance(item, int):  # year
            return reverse("circuit_year_view", kwargs={"year": item})

    def priority(self, item):
        if isinstance(item, int):  # year
            return 1 if item == settings.CURRENT_YEAR else 0.5

        if isinstance(item, Circuit):
            return 1 if item.pk in self.current_year_circuits else 0.5

    def changefreq(self, item):
        return "weekly"
