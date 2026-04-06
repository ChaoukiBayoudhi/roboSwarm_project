from rest_framework import serializers

from .models import Drone


class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = [
            "id",
            "name",
            "serial_number",
            "battery_level",
            "max_speed",
            "max_altitude",
            "is_autonomous",
            "payload_capacity",
        ]
        read_only_fields = ["id"]
