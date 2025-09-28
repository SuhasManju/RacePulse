from live_data.models import SessionLap, LapTelemetry
from Race.models import *
from RacePulse.utils import convert_timedelta_time, check_pd_na
import fastf1


def dump_to_db_session_lap(year, round_num, session_type):

    session = fastf1.get_session(
        year=year, gp=round_num, identifier=session_type.split("_")[0])

    driver_nums = RaceData.objects.filter(
        race__round=round_num, race__year_id=year, type=session_type).values_list("position_number", "driver_id", "race_id")

    if session_type in [RaceData.RACE_RESULT, RaceData.SPRINT_RACE_RESULT]:
        session.load(laps=True, telemetry=False, weather=False, messages=False)
    else:
        session.load()

    laps = session.laps

    for driver_num, driver_pk, race_id in driver_nums:
        driver_laps = laps.pick_drivers(str(driver_num))
        lap_nums = list(driver_laps['LapNumber'])

        for lap_num in lap_nums:
            driver_lap = driver_laps.pick_laps(lap_num)
            driver_lap_dict = driver_lap.iloc[0].to_dict()

            lap_obj = SessionLap(
                race_id=race_id,
                session_type=session_type,
                lap_time=convert_timedelta_time(driver_lap_dict['LapTime']),
                lap_number=check_pd_na(lap_num),
                pit_in_time=convert_timedelta_time(
                    driver_lap_dict['PitInTime']),
                pit_out_time=convert_timedelta_time(
                    driver_lap_dict['PitOutTime']),
                sector1_time=convert_timedelta_time(
                    driver_lap_dict['Sector1Time']),
                sector2_time=convert_timedelta_time(
                    driver_lap_dict['Sector2Time']),
                sector3_time=convert_timedelta_time(
                    driver_lap_dict['Sector3Time']),
                speed_i1=check_pd_na(driver_lap_dict['SpeedI1']),
                speed_i2=check_pd_na(driver_lap_dict['SpeedI2']),
                speed_fl=check_pd_na(driver_lap_dict['SpeedFL']),
                speed_st=check_pd_na(driver_lap_dict['SpeedST']),
                personal_best=check_pd_na(driver_lap_dict['IsPersonalBest']),
                compound=check_pd_na(driver_lap_dict['Compound']),
                tyre_life=check_pd_na(driver_lap_dict['TyreLife']),
                team=check_pd_na(driver_lap_dict['Team']),
                track_status=check_pd_na(driver_lap_dict["TrackStatus"]),
                position=check_pd_na(driver_lap_dict['Position']),
                deleted=check_pd_na(driver_lap_dict['Deleted']),
                deleted_reason=check_pd_na(driver_lap_dict['DeletedReason']),
                driver_pk=driver_pk,
            )
            lap_obj.save()

            if session_type in [RaceData.RACE_RESULT, RaceData.SPRINT_RACE_RESULT] or not driver_lap_dict['IsPersonalBest']:
                continue

            car_telemetry = driver_lap.get_car_data()

            telemetry_obj_list = []

            for _, telemetry in car_telemetry.iterrows():
                telemetry_obj = LapTelemetry(
                    lap_id=lap_obj.pk,
                    time_stamp=str(telemetry['Date']),
                    rpm=telemetry['RPM'],
                    speed=telemetry['Speed'],
                    gear=telemetry['nGear'],
                    throttle=telemetry['Throttle'],
                    brake=telemetry['Brake'],
                    drs=telemetry['DRS'],
                    session_time=convert_timedelta_time(
                        telemetry['SessionTime']),
                )
                telemetry_obj_list.append(telemetry_obj)

            LapTelemetry.objects.bulk_create(
                telemetry_obj_list, batch_size=200)
