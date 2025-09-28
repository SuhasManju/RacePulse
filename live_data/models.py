from django.db import models


class SessionLap(models.Model):

    TYRE_SOFT = "SOFT"
    TYRE_MEDIUM = "MEDIUM"
    TYRE_HARD = "HARD"
    TYRE_INTERMEDIATE = "INTERMEDIATE"
    TYRE_WET = "WET"
    TYRE_TEST_UNKNOWN = "TEST_UNKNOWN"
    TYRE_UNKNOWN = "UNKNOWN"

    race_id = models.IntegerField("Race Id")
    session_type = models.CharField("Session Type", max_length=100)

    driver_pk = models.CharField("Driver Pk", max_length=50)
    lap_time = models.TimeField("Lap Time", null=True)
    lap_number = models.IntegerField("Lap Number")
    pit_in_time = models.TimeField("Pit In Time", null=True)
    pit_out_time = models.TimeField("Pit Out Time", null=True)
    sector1_time = models.TimeField("Sector 1 Time", null=True)
    sector2_time = models.TimeField("Sector 2 Time", null=True)
    sector3_time = models.TimeField("Sector 3 Time", null=True)
    speed_i1 = models.FloatField("Speed trap 1", null=True)
    speed_i2 = models.FloatField("Speed Trap 2", null=True)
    speed_fl = models.FloatField("Speed Finish Line", null=True)
    speed_st = models.FloatField("Speed at Finish Line", null=True)
    personal_best = models.BooleanField(
        "Personal Best", default=False, null=True)
    compound = models.CharField("Compound", max_length=50, null=True)

    # No. of Laps on current Tyre
    tyre_life = models.IntegerField("Tyre Life", null=True)
    team = models.CharField("Team Name", max_length=50, null=True)
    track_status = models.CharField("Track Status", max_length=50, null=True)
    position = models.FloatField("Track Position", null=True)
    deleted = models.BooleanField("Lap Deleted", default=False, null=True)
    deleted_reason = models.CharField(
        "Deleted Reason", max_length=100, null=True)


class LapTelemetry(models.Model):

    lap = models.ForeignKey(
        SessionLap, on_delete=models.CASCADE, related_name="laps")

    time_stamp = models.DateTimeField("Time Stamp")
    rpm = models.FloatField("Engine RPM", null=True)
    speed = models.FloatField("Car Speed", null=True)
    gear = models.IntegerField("Transmission Gear", null=True)
    throttle = models.FloatField("Throttle", null=True)
    brake = models.BooleanField("Brake", default=False)
    drs = models.IntegerField("DRS status", null=True)

    session_time = models.TimeField("Session Time", null=True)
