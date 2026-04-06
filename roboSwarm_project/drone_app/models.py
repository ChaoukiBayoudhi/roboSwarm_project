import uuid

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class Drone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    battery_level = models.PositiveSmallIntegerField(
        default=100,
        validators=[
            MaxValueValidator(100, message="Battery level must be at most 100."),
            MinValueValidator(0, message="Battery level cannot be negative."),
        ],
    )
    max_speed = models.FloatField(
        default=10.0,
        validators=[MinValueValidator(0, message="max_speed must be zero or greater.")],
    )
    max_altitude = models.FloatField(
        default=100.0,
        validators=[MinValueValidator(0, message="max_altitude must be zero or greater.")],
    )
    is_autonomous = models.BooleanField(default=False)
    payload_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Maximum payload capacity in kg",
        validators=[MinValueValidator(0, message="payload_capacity cannot be negative.")],
    )

    class Meta:
        db_table = "drones"
        ordering = ["-max_altitude", "-payload_capacity"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["serial_number"]),
            models.Index(fields=["is_autonomous"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(battery_level__gte=0)
                & models.Q(battery_level__lte=100),
                name="drone_battery_level_0_100",
            ),
            models.CheckConstraint(
                condition=models.Q(max_altitude__gt=0) & models.Q(max_altitude__lte=10000),
                name="drone_max_altitude_0_10000",
            ),
            models.CheckConstraint(
                condition=models.Q(payload_capacity__gte=0),
                name="drone_payload_capacity_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.serial_number}"

    def clean(self):
        if self.is_autonomous and self.battery_level <= 20:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"battery_level": "Autonomous drones must have battery level > 20%."}
            )
