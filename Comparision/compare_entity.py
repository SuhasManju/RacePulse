from django.db.models import Q
from django.conf import settings
import pandas as pd
import numpy as np
from Race.models import RaceData


class CompareDriver:
    COLUMNS = ["type", "position_number", "constructor_id",
               "driver_id", "race_id", "race_points"]

    def __init__(self, year: int = settings.CURRENT_YEAR, driver_list: list = None):
        self.driver_list = driver_list
        self.year = year

    def make_context_dict(self):
        df = self.make_qs()

        raced_list = [set(df[df["driver_id"] == driver]["race_id"])
                      for driver in self.driver_list]

        common_races = set.intersection(*raced_list)
        df = df[df['race_id'].isin(common_races)]

        if df.empty:
            return {}

        sprint_quali = self.head_vs_head(df, RaceData.SPRINT_QUALIFYING_RESULT)
        quali = self.head_vs_head(df, RaceData.QUALIFYING_RESULT)
        race = self.head_vs_head(df, RaceData.RACE_RESULT)
        sprint_race = self.head_vs_head(df, RaceData.SPRINT_RACE_RESULT)

        driver1 = self.driver_list[0]
        driver2 = self.driver_list[1]

        driver1_dict = {
            "sprintQuali": sprint_quali[driver1][0],
            "sprintQualiPoles": sprint_quali[driver1][2],
            "quali": quali[driver1][0],
            "qualiPoles": quali[driver1][2],
            "sprintRace": sprint_race[driver1][0],
            "sprintDnf": sprint_race[driver1][1],
            "sprintWins": sprint_race[driver1][2],
            "race": race[driver1][0],
            "raceDnf": race[driver1][1],
            "raceWins": race[driver1][2],
        }

        driver2_dict = {
            "sprintQuali": sprint_quali[driver2][0],
            "sprintQualiPoles": sprint_quali[driver2][2],
            "quali": quali[driver2][0],
            "qualiPoles": quali[driver2][2],
            "sprintRace": sprint_race[driver2][0],
            "sprintDnf": sprint_race[driver2][1],
            "sprintWins": sprint_race[driver2][2],
            "race": race[driver2][0],
            "raceDnf": race[driver2][1],
            "raceWins": race[driver2][2],
        }

        return {"noOfRaces": len(common_races), driver1: driver1_dict, driver2: driver2_dict}

    def make_qs(self):
        qs = Q(race__year_id=self.year)
        qs &= Q(type__in=[RaceData.RACE_RESULT, RaceData.SPRINT_QUALIFYING_RESULT,
                RaceData.QUALIFYING_RESULT, RaceData.SPRINT_RACE_RESULT])
        qs &= Q(driver_id__in=self.driver_list)

        result = RaceData.objects.filter(qs).values_list(*self.COLUMNS)

        df = pd.DataFrame(result, columns=self.COLUMNS)
        df = df.replace(np.nan, 0)
        return df

    def head_vs_head(self, df, race_type):
        df = df[df['type'] == race_type]

        driver1 = self.driver_list[0]
        driver2 = self.driver_list[1]

        race1 = df[df['driver_id'] == driver1][['race_id', 'position_number']].rename(
            columns={"position_number": "pos1"})
        race2 = df[df['driver_id'] == driver2][['race_id', 'position_number']].rename(
            columns={"position_number": "pos2"})

        merged = pd.merge(race1, race2, on='race_id')

        d1_vs_d2 = (merged['pos1'] < merged['pos2']).sum()
        d2_vs_d1 = (merged['pos2'] < merged['pos1']).sum()
        d1_dnf = (merged['pos1'] == 0).sum()
        d2_dnf = (merged['pos2'] == 0).sum()
        d1_wins = (merged['pos1'] == 1).sum()
        d2_wins = (merged['pos2'] == 1).sum()

        return {driver1: [d1_vs_d2, d1_dnf, d1_wins], driver2: [d2_vs_d1, d2_dnf, d2_wins]}


class CompareTeam(CompareDriver):
    def make_qs(self):
        qs = Q(race__year_id=self.year)
        qs &= Q(type__in=[RaceData.RACE_RESULT, RaceData.SPRINT_QUALIFYING_RESULT,
                RaceData.QUALIFYING_RESULT, RaceData.SPRINT_RACE_RESULT])
        qs &= Q(constructor_id__in=self.driver_list)

        result = RaceData.objects.filter(qs).values_list(*self.COLUMNS)

        df = pd.DataFrame(result, columns=self.COLUMNS)
        df = df.replace(np.nan, 0)
        print(df.empty)

        # Droping driver column and replacing it constrcutor with driver to reuse the above code
        df = df.drop("driver_id", axis=1)
        df = df.rename(columns={"constructor_id": "driver_id"})
        return df
