from rest_framework import serializers

from .models import Mission, MissionParticipation, Task, TechnicalSpecification, TelemetryRecord


class TechnicalSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnicalSpecification
        fields = [
            "id",
            "robot",
            "drone",
            "cpu",
            "memory_gb",
            "firmware_version",
        ]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "mission", "title", "priority", "is_completed"]


class MissionSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = [
            "id",
            "name",
            "description",
            "start_time",
            "end_time",
            "status",
            "tasks",
        ]


class MissionParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionParticipation
        fields = ["id", "mission", "agent_id", "role", "assigned_at"]
        read_only_fields = ["id", "assigned_at"]


class TelemetryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelemetryRecord
        fields = ["id", "agent_id", "timestamp", "data"]
