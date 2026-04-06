from django.contrib import admin
from .models import (
    Mission,
    MissionParticipation,
    Task,
    TechnicalSpecification,
    TelemetryRecord,
)

admin.site.register(TechnicalSpecification)
admin.site.register(Mission)
admin.site.register(Task)
admin.site.register(MissionParticipation)
admin.site.register(TelemetryRecord)