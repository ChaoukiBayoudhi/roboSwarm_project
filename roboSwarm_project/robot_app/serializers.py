from rest_framework import serializers

from .models import Robot


class RobotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Robot
        fields = [
            "id",
            "name",
            "serial_number",
            "battery_level",
            "max_speed",
            "is_active",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
