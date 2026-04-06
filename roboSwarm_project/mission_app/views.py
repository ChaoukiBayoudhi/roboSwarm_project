from rest_framework import viewsets

from .models import Mission, MissionParticipation, Task, TechnicalSpecification, TelemetryRecord
from .serializers import (
    MissionSerializer,
    MissionParticipationSerializer,
    TaskSerializer,
    TechnicalSpecificationSerializer,
    TelemetryRecordSerializer,
)


class TechnicalSpecificationViewSet(viewsets.ModelViewSet):
    queryset = TechnicalSpecification.objects.select_related("robot", "drone").all()
    serializer_class = TechnicalSpecificationSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.prefetch_related("tasks", "participations").all()
    serializer_class = MissionSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("mission").all()
    serializer_class = TaskSerializer


class MissionParticipationViewSet(viewsets.ModelViewSet):
    queryset = MissionParticipation.objects.select_related("mission").all()
    serializer_class = MissionParticipationSerializer


class TelemetryRecordViewSet(viewsets.ModelViewSet):
    queryset = TelemetryRecord.objects.all()
    serializer_class = TelemetryRecordSerializer
