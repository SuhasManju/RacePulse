from django.contrib import admin
from live_data.models import SessionLap, LapTelemetry


@admin.register(SessionLap)
class SessionLapAdmin(admin.ModelAdmin):
    list_display = ['pk', 'race_id', 'session_type',
                    'driver_pk', 'lap_number', 'lap_time',]
    list_filter = ['session_type']
