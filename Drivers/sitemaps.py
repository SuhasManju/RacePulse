from django.contrib.sitemaps import Sitemap
from Race.models import Driver, SeasonDriver
from django.urls import reverse
from django.conf import settings


class DriverSiteMap(Sitemap):

    def __init__(self):
        super().__init__()
        self.current_year_drivers = SeasonDriver.objects.filter(
            year_id=settings.CURRENT_YEAR).values_list("driver_id", flat=True)

    def items(self):
        drivers = Driver.objects.all().only("pk")
        years = range(settings.MIN_YEAR, settings.CURRENT_YEAR + 1)

        # Combine both constructors and years into one iterable
        return list(drivers) + list(years)

    def location(self, item):
        if isinstance(item, Driver):
            return reverse("drivers_detailed_view", kwargs={"driverId": item.pk})
        elif isinstance(item, int):  # year
            return reverse("drivers_home_page", kwargs={"year": item})

    def priority(self, item):
        if isinstance(item, int):  # year
            return 1 if item == settings.CURRENT_YEAR else 0.5

        if isinstance(item, Driver):
            return 1 if item.pk in self.current_year_drivers else 0.5

    def changefreq(self, item):
        return "weekly"
