import uuid
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from .models import Mission, MissionParticipation, Task, TechnicalSpecification, TelemetryRecord
from .serializers import (
    MissionSerializer,
    MissionParticipationSerializer,
    TaskSerializer,
    TechnicalSpecificationSerializer,
    TelemetryRecordSerializer,
)
from rest_framework.decorators import action


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

    #3rd case : value as body parameter
    #update the missions of a given agent_id
    #to call the endpoint:
    #http://127.0.0.1:8000/api/mission-participations/update/123e4567-e89b-12d3-a456-426614174000/
    #the 123e4567-e89b-12d3-a456-426614174000 is the agent_id
    #[^/.] means any character except / and .
    #regex to check if the agent_id is a valid UUID
    #^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$
    @action(detail=False, methods=["PUT", "PATCH"], url_path=r"update/(?P<agent_id>[^/.]+)")
    def update_missions_of_agent(self, request, agent_id):
        #check if the agent_id is a valid UUID
        try:
            agent_uuid = uuid.UUID(str(agent_id))
        except (TypeError, ValueError):
            return Response(
                {"detail": f"Invalid agent_id UUID: {agent_id}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Missions linked to this agent through participations
        missions = Mission.objects.filter(participations__agent_id=agent_uuid).distinct()
        if not missions.exists():
            return Response(
                f"No missions found for agent_id: {agent_uuid}",
                status=status.HTTP_204_NO_CONTENT,
            )
        #get the status, and dates (start_time, end_time) from the request body or default to None
        new_status = request.data.get("status", None)
        new_start_time_raw = request.data.get("start_time", None)
        new_end_time_raw = request.data.get("end_time", None)

        if request.method == "PUT" and (new_status is None or new_start_time_raw is None or new_end_time_raw is None):
            return Response(
                {"detail": "PUT requires 'status', 'start_time', and 'end_time'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_start_time = None
        if new_start_time_raw is not None:
            new_start_time = parse_datetime(str(new_start_time_raw))
            if new_start_time is None:
                return Response(
                    {"detail": f"Invalid start_time datetime: {new_start_time_raw}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        new_end_time = None
        if new_end_time_raw is not None:
            new_end_time = parse_datetime(str(new_end_time_raw))
            if new_end_time is None:
                return Response(
                    {"detail": f"Invalid end_time datetime: {new_end_time_raw}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if new_start_time is not None and new_end_time is not None and new_start_time >= new_end_time:
            return Response(
                {"detail": "start_time must be before end_time."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_status is None and new_start_time is None and new_end_time is None:
            return Response(
                {"detail": "Provide at least one of: status, start_time, end_time."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        update_fields = {}
        if new_status is not None:
            update_fields["status"] = new_status
        if new_start_time is not None:
            update_fields["start_time"] = new_start_time
        if new_end_time is not None:
            update_fields["end_time"] = new_end_time

        missions.update(**update_fields)
        #return the updated missions
        updated = list(missions)
        return Response(MissionSerializer(updated, many=True).data, status=status.HTTP_200_OK)


class TelemetryRecordViewSet(viewsets.ModelViewSet):
    queryset = TelemetryRecord.objects.all()
    serializer_class = TelemetryRecordSerializer
