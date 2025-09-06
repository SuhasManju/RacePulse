from django.contrib.sitemaps import Sitemap
from Race.models import Constructor, SeasonConstructor
from django.urls import reverse
from django.conf import settings


class RaceSiteMap(Sitemap):

    def __init__(self):
        super().__init__()
        self.current_year_constructors = SeasonConstructor.objects.filter(
            year_id=settings.CURRENT_YEAR).values_list("constructor_id", flat=True)

    def items(self):
        teams = Constructor.objects.all().only("pk")
        years = range(settings.MIN_YEAR, settings.CURRENT_YEAR + 1)

        # Combine both constructors and years into one iterable
        return list(teams) + list(years)

    def location(self, item):
        if isinstance(item, Constructor):
            return reverse("team_page", kwargs={"teamId": item.pk})
        elif isinstance(item, int):  # year
            return reverse("team_home_page", kwargs={"year": item})

    def priority(self, item):
        if isinstance(item, int):  # year
            return 1 if item == settings.CURRENT_YEAR else 0.5

        if isinstance(item, Constructor):
            return 1 if item.pk in self.current_year_constructors else 0.5

        return 1  # for constructors

    def changefreq(self, item):
        return "weekly"
