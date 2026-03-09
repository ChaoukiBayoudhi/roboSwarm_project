from django.db import models
from django.db.models.fields import uuid


class Drone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    battery_level = models.PositiveSmallIntegerField(default=100)
    max_speed = models.FloatField(default=10.0)
    max_altitude = models.FloatField(default=100.0)
    is_autonomous = models.BooleanField(default=False)
    status = models.CharField(max_length=100)
    payload_capacity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.0,
        help_text="Maximum payload capacity in kg",
    )
    class Meta:
        db_table = 'drones'
        ordering = ['-max_altitude', '-payload_capacity']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['serial_number']),
        ]
        