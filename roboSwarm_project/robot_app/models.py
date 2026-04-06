import uuid

from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models


class Robot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    battery_level = models.PositiveSmallIntegerField(
        default=100,
        validators=[
            MaxValueValidator(100, message="Battery level must be less than or equal to 100."),
            MinValueValidator(0, message="Battery level cannot be negative."),
        ],
    )
    max_speed = models.FloatField(
        default=10.0,
        validators=[MinValueValidator(0, message="max_speed must be zero or greater.")],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "robots"
        ordering = ["-max_speed"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["serial_number"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(battery_level__gte=0)
                & models.Q(battery_level__lte=100),
                name="robot_battery_level_0_100",
            ),
            models.CheckConstraint(
                condition=models.Q(max_speed__gte=0),
                name="robot_max_speed_non_negative",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.serial_number}"

    def clean(self):
        if self.is_active and self.battery_level <= 10:
            from django.core.exceptions import ValidationError

            raise ValidationError(
                {"battery_level": "Active robots must have battery level > 10%."}
            )
