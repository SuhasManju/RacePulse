# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from RacePulse.utils import *
from django.templatetags.static import static
from functools import cached_property

class Chassis(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    constructor = models.ForeignKey("Constructor", models.DO_NOTHING)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "chassis"


class Circuit(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    previous_names = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=6)
    direction = models.CharField(max_length=14)
    place_name = models.CharField(max_length=100)
    country = models.ForeignKey("Country", models.DO_NOTHING)
    latitude = models.DecimalField(max_digits=10, decimal_places=6)
    longitude = models.DecimalField(max_digits=10, decimal_places=6)
    length = models.DecimalField(max_digits=6, decimal_places=3)
    turns = models.IntegerField()
    total_races_held = models.IntegerField()

    class Meta:
        managed = False
        db_table = "circuit"

    @cached_property
    def circuit_image(self):
        return static(f"circuit_img/{self.pk}.avif")


class Constructor(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    country = models.ForeignKey("Country", models.DO_NOTHING)
    best_championship_position = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_championship_wins = models.IntegerField()
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_1_and_2_finishes = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_championship_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = "constructor"

    @cached_property
    def team_img(self):
        return static(f"team_img/{self.pk}.avif")

    @cached_property
    def team_sm_img(self):
        return static(f"team_sm_img/{self.pk}.avif")

    @cached_property
    def team_color(self):
        return TEAM_COLOR_DICT.get(self.pk)


class ConstructorChronology(models.Model):
    pk = models.CompositePrimaryKey("constructor_id", "position_display_order")
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    position_display_order = models.IntegerField()
    other_constructor = models.ForeignKey(
        Constructor,
        models.DO_NOTHING,
        related_name="constructorchronology_other_constructor_set",
    )
    year_from = models.IntegerField()
    year_to = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "constructor_chronology"
        unique_together = (
            ("constructor", "position_display_order"),
            ("constructor", "other_constructor", "year_from", "year_to"),
        )


class Continent(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    code = models.CharField(unique=True, max_length=2)
    name = models.CharField(unique=True, max_length=100)
    demonym = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "continent"


class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    alpha2_code = models.CharField(unique=True, max_length=2)
    alpha3_code = models.CharField(unique=True, max_length=3)
    name = models.CharField(unique=True, max_length=100)
    demonym = models.CharField(max_length=100, blank=True, null=True)
    continent = models.ForeignKey(Continent, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "country"


class Driver(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=3)
    permanent_number = models.CharField(max_length=2, blank=True, null=True)
    gender = models.CharField(max_length=6)
    date_of_birth = models.DateField()
    date_of_death = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=100)
    country_of_birth_country = models.ForeignKey(Country, models.DO_NOTHING)
    nationality_country = models.ForeignKey(
        Country, models.DO_NOTHING, related_name="driver_nationality_country_set"
    )
    second_nationality_country = models.ForeignKey(
        Country,
        models.DO_NOTHING,
        related_name="driver_second_nationality_country_set",
        blank=True,
        null=True,
    )
    best_championship_position = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_championship_wins = models.IntegerField()
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_championship_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()
    total_driver_of_the_day = models.IntegerField()
    total_grand_slams = models.IntegerField()

    class Meta:
        managed = False
        db_table = "driver"

    @cached_property
    def driver_img(self):
        return static(f"driver_img/{self.pk}.avif")


class DriverFamilyRelationship(models.Model):
    pk = models.CompositePrimaryKey("driver_id", "position_display_order")
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    position_display_order = models.IntegerField()
    other_driver = models.ForeignKey(
        Driver,
        models.DO_NOTHING,
        related_name="driverfamilyrelationship_other_driver_set",
    )
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = "driver_family_relationship"
        unique_together = (
            ("driver", "position_display_order"),
            ("driver", "other_driver", "type"),
        )

    @cached_property
    def driver_relation(self):
        relation = self.type.replace("_", " ")
        relation.replace("in law", "in-law")
        return relation.title()


class Engine(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    engine_manufacturer = models.ForeignKey("EngineManufacturer", models.DO_NOTHING)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    capacity = models.DecimalField(
        max_digits=2, decimal_places=1, blank=True, null=True
    )
    configuration = models.CharField(max_length=100, blank=True, null=True)
    aspiration = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "engine"


class EngineManufacturer(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    best_championship_position = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_championship_wins = models.IntegerField()
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_championship_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = "engine_manufacturer"


class Entrant(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "entrant"


class GrandPrix(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=3)
    country = models.ForeignKey(Country, models.DO_NOTHING, blank=True, null=True)
    total_races_held = models.IntegerField()

    class Meta:
        managed = False
        db_table = "grand_prix"


class Race(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.ForeignKey("Season", models.DO_NOTHING, db_column="year")
    round = models.IntegerField()
    date = models.DateField()
    time = models.TextField(blank=True, null=True)
    grand_prix = models.ForeignKey(GrandPrix, models.DO_NOTHING)
    official_name = models.CharField(max_length=100)
    qualifying_format = models.CharField(max_length=20)
    sprint_qualifying_format = models.CharField(max_length=20, blank=True, null=True)
    circuit = models.ForeignKey(Circuit, models.DO_NOTHING)
    circuit_type = models.CharField(max_length=6)
    direction = models.CharField(max_length=14)
    course_length = models.DecimalField(max_digits=6, decimal_places=3)
    turns = models.IntegerField()
    laps = models.IntegerField()
    distance = models.DecimalField(max_digits=6, decimal_places=3)
    scheduled_laps = models.IntegerField(blank=True, null=True)
    scheduled_distance = models.DecimalField(
        max_digits=6, decimal_places=3, blank=True, null=True
    )
    drivers_championship_decider = models.IntegerField(blank=True, null=True)
    constructors_championship_decider = models.IntegerField(blank=True, null=True)
    pre_qualifying_date = models.DateField(blank=True, null=True)
    pre_qualifying_time = models.CharField(max_length=5, blank=True, null=True)
    free_practice_1_date = models.DateField(blank=True, null=True)
    free_practice_1_time = models.CharField(max_length=5, blank=True, null=True)
    free_practice_2_date = models.DateField(blank=True, null=True)
    free_practice_2_time = models.CharField(max_length=5, blank=True, null=True)
    free_practice_3_date = models.DateField(blank=True, null=True)
    free_practice_3_time = models.CharField(max_length=5, blank=True, null=True)
    free_practice_4_date = models.DateField(blank=True, null=True)
    free_practice_4_time = models.CharField(max_length=5, blank=True, null=True)
    qualifying_1_date = models.DateField(blank=True, null=True)
    qualifying_1_time = models.CharField(max_length=5, blank=True, null=True)
    qualifying_2_date = models.DateField(blank=True, null=True)
    qualifying_2_time = models.CharField(max_length=5, blank=True, null=True)
    qualifying_date = models.DateField(blank=True, null=True)
    qualifying_time = models.CharField(max_length=5, blank=True, null=True)
    sprint_qualifying_date = models.DateField(blank=True, null=True)
    sprint_qualifying_time = models.CharField(max_length=5, blank=True, null=True)
    sprint_race_date = models.DateField(blank=True, null=True)
    sprint_race_time = models.CharField(max_length=5, blank=True, null=True)
    warming_up_date = models.DateField(blank=True, null=True)
    warming_up_time = models.CharField(max_length=5, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "race"
        unique_together = (("year", "round"),)

    @cached_property
    def is_sprint(self):
        # checking whether the week is a sprint
        if self.sprint_qualifying_date:
            return True
        return False

    @cached_property
    def fp1_time(self):
        return combine_datetime(self.free_practice_1_date, self.free_practice_1_time)

    @cached_property
    def fp2_time(self):
        return combine_datetime(self.free_practice_2_date, self.free_practice_2_time)

    @cached_property
    def fp3_time(self):
        return combine_datetime(self.free_practice_3_date, self.free_practice_3_time)

    @cached_property
    def sprint_time(self):
        return combine_datetime(self.sprint_race_date, self.sprint_race_time)

    @cached_property
    def sprint_quali_time(self):
        return combine_datetime(
            self.sprint_qualifying_date, self.sprint_qualifying_time
        )

    @cached_property
    def quali_time(self):
        return combine_datetime(self.qualifying_date, self.qualifying_time)

    @cached_property
    def race_time(self):
        return combine_datetime(self.date, self.time)

    @cached_property
    def event_date(self):
        fp1_date = self.free_practice_1_date
        race_date = self.date

        if fp1_date.month == race_date.month:
            # Same month: May 12–14 2025
            return f"{fp1_date.strftime('%b')} {fp1_date.day} – {race_date.day} {race_date.year}"
        else:
            # Cross month: May 30 – June 2 2025
            return f"{fp1_date.strftime('%b')} {fp1_date.day} – {race_date.strftime('%b')} {race_date.day} {race_date.year}"

    @cached_property
    def available_events(self):
        data_map = [
            (self.fp1_time, "FP1"),
            (self.sprint_quali_time, "Sprint Qualifying"),
            (self.fp2_time, "FP2"),
            (self.fp3_time, "FP3"),
            (self.sprint_time, "Sprint"),
            (self.quali_time, "Qualifying"),
            (self.race_time, "Race")
        ]

        available_data = [(label, time) for time, label in data_map if time]
        return available_data

    @cached_property
    def next_event(self):
        data_map = [
            (self.fp1_time, "FP1"),
            (self.sprint_quali_time, "Sprint Qualifying"),
            (self.fp2_time, "FP2"),
            (self.fp3_time, "FP3"),
            (self.sprint_time, "Sprint"),
            (self.quali_time, "Qualifying"),
            (self.race_time, "Race")
        ]
        now = timezone.now()
        next_event = [None, None]
        for event in data_map:
            if event[0] and event[0] > now:
                next_event = event
                break
        return next_event


class RaceConstructorStanding(models.Model):
    pk = models.CompositePrimaryKey("race_id", "position_display_order")
    race = models.ForeignKey(Race, models.DO_NOTHING)
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    points = models.DecimalField(max_digits=8, decimal_places=2)
    positions_gained = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "race_constructor_standing"
        unique_together = (("race", "position_display_order"),)


class RaceData(models.Model):

    # Types model choices
    DRIVER_OF_THE_DAY_RESULT = 'DRIVER_OF_THE_DAY_RESULT'
    FASTEST_LAP = 'FASTEST_LAP'
    FREE_PRACTICE_1_RESULT = 'FREE_PRACTICE_1_RESULT'
    FREE_PRACTICE_2_RESULT = 'FREE_PRACTICE_2_RESULT'
    FREE_PRACTICE_3_RESULT = 'FREE_PRACTICE_3_RESULT'
    FREE_PRACTICE_4_RESULT = 'FREE_PRACTICE_4_RESULT'
    PIT_STOP = 'PIT_STOP'
    PRE_QUALIFYING_RESULT = 'PRE_QUALIFYING_RESULT'
    QUALIFYING_1_RESULT = 'QUALIFYING_1_RESULT'
    QUALIFYING_2_RESULT = 'QUALIFYING_2_RESULT'
    QUALIFYING_RESULT = 'QUALIFYING_RESULT'
    RACE_RESULT = 'RACE_RESULT'
    SPRINT_QUALIFYING_RESULT = 'SPRINT_QUALIFYING_RESULT'
    SPRINT_RACE_RESULT = 'SPRINT_RACE_RESULT'
    SPRINT_STARTING_GRID_POSITION = 'SPRINT_STARTING_GRID_POSITION'
    STARTING_GRID_POSITION = 'STARTING_GRID_POSITION'
    WARMING_UP_RESULT = 'WARMING_UP_RESULT'


    pk = models.CompositePrimaryKey("race_id", "type", "position_display_order")
    race = models.ForeignKey(Race, models.DO_NOTHING)
    type = models.CharField(max_length=50)
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4)
    driver_number = models.CharField(max_length=3)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    tyre_manufacturer = models.ForeignKey("TyreManufacturer", models.DO_NOTHING)
    practice_time = models.CharField(max_length=20, blank=True, null=True)
    practice_time_millis = models.IntegerField(blank=True, null=True)
    practice_gap = models.CharField(max_length=20, blank=True, null=True)
    practice_gap_millis = models.IntegerField(blank=True, null=True)
    practice_interval = models.CharField(max_length=20, blank=True, null=True)
    practice_interval_millis = models.IntegerField(blank=True, null=True)
    practice_laps = models.IntegerField(blank=True, null=True)
    qualifying_time = models.CharField(max_length=20, blank=True, null=True)
    qualifying_time_millis = models.IntegerField(blank=True, null=True)
    qualifying_q1 = models.CharField(max_length=20, blank=True, null=True)
    qualifying_q1_millis = models.IntegerField(blank=True, null=True)
    qualifying_q2 = models.CharField(max_length=20, blank=True, null=True)
    qualifying_q2_millis = models.IntegerField(blank=True, null=True)
    qualifying_q3 = models.CharField(max_length=20, blank=True, null=True)
    qualifying_q3_millis = models.IntegerField(blank=True, null=True)
    qualifying_gap = models.CharField(max_length=20, blank=True, null=True)
    qualifying_gap_millis = models.IntegerField(blank=True, null=True)
    qualifying_interval = models.CharField(max_length=20, blank=True, null=True)
    qualifying_interval_millis = models.IntegerField(blank=True, null=True)
    qualifying_laps = models.IntegerField(blank=True, null=True)
    starting_grid_position_qualification_position_number = models.IntegerField(
        blank=True, null=True
    )
    starting_grid_position_qualification_position_text = models.CharField(
        max_length=4, blank=True, null=True
    )
    starting_grid_position_grid_penalty = models.CharField(
        max_length=20, blank=True, null=True
    )
    starting_grid_position_grid_penalty_positions = models.IntegerField(
        blank=True, null=True
    )
    starting_grid_position_time = models.CharField(max_length=20, blank=True, null=True)
    starting_grid_position_time_millis = models.IntegerField(blank=True, null=True)
    race_shared_car = models.IntegerField(blank=True, null=True)
    race_laps = models.IntegerField(blank=True, null=True)
    race_time = models.CharField(max_length=20, blank=True, null=True)
    race_time_millis = models.IntegerField(blank=True, null=True)
    race_time_penalty = models.CharField(max_length=20, blank=True, null=True)
    race_time_penalty_millis = models.IntegerField(blank=True, null=True)
    race_gap = models.CharField(max_length=20, blank=True, null=True)
    race_gap_millis = models.IntegerField(blank=True, null=True)
    race_gap_laps = models.IntegerField(blank=True, null=True)
    race_interval = models.CharField(max_length=20, blank=True, null=True)
    race_interval_millis = models.IntegerField(blank=True, null=True)
    race_reason_retired = models.CharField(max_length=100, blank=True, null=True)
    race_points = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True
    )
    race_pole_position = models.IntegerField(blank=True, null=True)
    race_qualification_position_number = models.IntegerField(blank=True, null=True)
    race_qualification_position_text = models.CharField(
        max_length=4, blank=True, null=True
    )
    race_grid_position_number = models.IntegerField(blank=True, null=True)
    race_grid_position_text = models.CharField(max_length=2, blank=True, null=True)
    race_positions_gained = models.IntegerField(blank=True, null=True)
    race_pit_stops = models.IntegerField(blank=True, null=True)
    race_fastest_lap = models.IntegerField(blank=True, null=True)
    race_driver_of_the_day = models.IntegerField(blank=True, null=True)
    race_grand_slam = models.IntegerField(blank=True, null=True)
    fastest_lap_lap = models.IntegerField(blank=True, null=True)
    fastest_lap_time = models.CharField(max_length=20, blank=True, null=True)
    fastest_lap_time_millis = models.IntegerField(blank=True, null=True)
    fastest_lap_gap = models.CharField(max_length=20, blank=True, null=True)
    fastest_lap_gap_millis = models.IntegerField(blank=True, null=True)
    fastest_lap_interval = models.CharField(max_length=20, blank=True, null=True)
    fastest_lap_interval_millis = models.IntegerField(blank=True, null=True)
    pit_stop_stop = models.IntegerField(blank=True, null=True)
    pit_stop_lap = models.IntegerField(blank=True, null=True)
    pit_stop_time = models.CharField(max_length=20, blank=True, null=True)
    pit_stop_time_millis = models.IntegerField(blank=True, null=True)
    driver_of_the_day_percentage = models.DecimalField(
        max_digits=4, decimal_places=1, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "race_data"
        unique_together = (("race", "type", "position_display_order"),)


class RaceDriverStanding(models.Model):
    pk = models.CompositePrimaryKey("race_id", "position_display_order")
    race = models.ForeignKey(Race, models.DO_NOTHING)
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    points = models.DecimalField(max_digits=8, decimal_places=2)
    positions_gained = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "race_driver_standing"
        unique_together = (("race", "position_display_order"),)


class Season(models.Model):
    year = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = "season"


class SeasonConstructor(models.Model):
    pk = models.CompositePrimaryKey("year", "constructor_id")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4, blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_1_and_2_finishes = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = "season_constructor"
        unique_together = (("year", "constructor"),)


class SeasonConstructorStanding(models.Model):
    pk = models.CompositePrimaryKey("year", "position_display_order")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    points = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = "season_constructor_standing"
        unique_together = (("year", "position_display_order"),)


class SeasonDriver(models.Model):
    pk = models.CompositePrimaryKey("year", "driver_id")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4, blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()
    total_driver_of_the_day = models.IntegerField()
    total_grand_slams = models.IntegerField()

    class Meta:
        managed = False
        db_table = "season_driver"
        unique_together = (("year", "driver"),)


class SeasonDriverStanding(models.Model):
    pk = models.CompositePrimaryKey("year", "position_display_order")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    points = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        managed = False
        db_table = "season_driver_standing"
        unique_together = (("year", "position_display_order"),)


class SeasonEngineManufacturer(models.Model):
    pk = models.CompositePrimaryKey("year", "engine_manufacturer_id")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=4, blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_points = models.DecimalField(max_digits=8, decimal_places=2)
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = "season_engine_manufacturer"
        unique_together = (("year", "engine_manufacturer"),)


class SeasonEntrant(models.Model):
    pk = models.CompositePrimaryKey("year", "entrant_id")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    entrant = models.ForeignKey(Entrant, models.DO_NOTHING)
    country = models.ForeignKey(Country, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "season_entrant"
        unique_together = (("year", "entrant"),)


class SeasonEntrantChassis(models.Model):
    pk = models.CompositePrimaryKey(
        "year", "entrant_id", "constructor_id", "engine_manufacturer_id", "chassis_id"
    )
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    entrant = models.ForeignKey(Entrant, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    chassis = models.ForeignKey(Chassis, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "season_entrant_chassis"
        unique_together = (
            ("year", "entrant", "constructor", "engine_manufacturer", "chassis"),
        )

    @cached_property
    def car_image(self):
        return static(f"team_car_image/{self.year_id}/{self.constructor_id}.avif")


class SeasonEntrantConstructor(models.Model):
    pk = models.CompositePrimaryKey(
        "year", "entrant_id", "constructor_id", "engine_manufacturer_id"
    )
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    entrant = models.ForeignKey(Entrant, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "season_entrant_constructor"
        unique_together = (("year", "entrant", "constructor", "engine_manufacturer"),)


class SeasonEntrantDriver(models.Model):
    pk = models.CompositePrimaryKey(
        "year", "entrant_id", "constructor_id", "engine_manufacturer_id", "driver_id"
    )
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    entrant = models.ForeignKey(Entrant, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    rounds = models.CharField(max_length=100, blank=True, null=True)
    rounds_text = models.CharField(max_length=100, blank=True, null=True)
    test_driver = models.IntegerField()

    class Meta:
        managed = False
        db_table = "season_entrant_driver"
        unique_together = (
            ("year", "entrant", "constructor", "engine_manufacturer", "driver"),
        )


class SeasonEntrantEngine(models.Model):
    pk = models.CompositePrimaryKey(
        "year", "entrant_id", "constructor_id", "engine_manufacturer_id", "engine_id"
    )
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    entrant = models.ForeignKey(Entrant, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    engine = models.ForeignKey(Engine, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "season_entrant_engine"
        unique_together = (
            ("year", "entrant", "constructor", "engine_manufacturer", "engine"),
        )


class SeasonEntrantTyreManufacturer(models.Model):
    pk = models.CompositePrimaryKey(
        "year",
        "entrant_id",
        "constructor_id",
        "engine_manufacturer_id",
        "tyre_manufacturer_id",
    )
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    entrant = models.ForeignKey(Entrant, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    tyre_manufacturer = models.ForeignKey("TyreManufacturer", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "season_entrant_tyre_manufacturer"
        unique_together = (
            (
                "year",
                "entrant",
                "constructor",
                "engine_manufacturer",
                "tyre_manufacturer",
            ),
        )


class SeasonTyreManufacturer(models.Model):
    pk = models.CompositePrimaryKey("year", "tyre_manufacturer_id")
    year = models.ForeignKey(Season, models.DO_NOTHING, db_column="year")
    tyre_manufacturer = models.ForeignKey("TyreManufacturer", models.DO_NOTHING)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = "season_tyre_manufacturer"
        unique_together = (("year", "tyre_manufacturer"),)


class TyreManufacturer(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, models.DO_NOTHING)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = "tyre_manufacturer"
