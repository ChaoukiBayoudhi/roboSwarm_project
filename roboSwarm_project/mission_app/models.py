import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from drone_app.models import Drone
from enumerations.enums import MissionRole, MissionStatus
from robot_app.models import Robot


class TechnicalSpecification(models.Model):
    id = models.AutoField(primary_key=True)
    robot = models.OneToOneField(
        Robot,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="technical_specification",
    )
    drone = models.OneToOneField(
        Drone,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="technical_specification",
    )
    cpu = models.CharField(max_length=100)
    memory_gb = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1, message="memory_gb must be greater than 0.")],
    )
    firmware_version = models.CharField(max_length=100)

    class Meta:
        db_table = "technical_specifications"
        ordering = ["-memory_gb", "cpu"]
        indexes = [
            models.Index(fields=["cpu"]),
            models.Index(fields=["memory_gb"]),
            models.Index(fields=["firmware_version"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=(
                    (models.Q(robot__isnull=False) & models.Q(drone__isnull=True))
                    | (models.Q(robot__isnull=True) & models.Q(drone__isnull=False))
                ),
                name="techspec_exactly_one_parent",
            ),
            models.CheckConstraint(
                condition=models.Q(memory_gb__gt=0),
                name="techspec_memory_gb_positive",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.cpu} ({self.memory_gb} GB RAM)"

    def clean(self):
        has_robot = self.robot_id is not None
        has_drone = self.drone_id is not None
        if has_robot == has_drone:
            raise ValidationError(
                "Link exactly one of robot or drone to a technical specification."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Mission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(7, message="Name must be at least 7 characters long.")
        ],
    )
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=100,
        choices=MissionStatus.choices,
        default=MissionStatus.PENDING,
    )

    class Meta:
        db_table = "missions"
        ordering = ["-start_time", "-end_time"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["start_time"]),
            models.Index(fields=["end_time"]),
            models.Index(fields=["status"]),
            models.Index(fields=["status", "start_time"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "start_time", "end_time"],
                name="unique_mission",
            ),
            models.CheckConstraint(
                condition=models.Q(end_time__gt=models.F("start_time")),
                name="mission_end_after_start",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.start_time} - {self.end_time} - {self.status}"

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(
                {"start_time": "Start time must be before end time."}
            )

    def get_participants(self):
        return self.participations.all()

    def save(self, *args, **kwargs):
        if self.pk and self.status == MissionStatus.ACTIVE and not self.participations.exists():
            raise ValidationError(
                {"status": "Mission must have at least one participant before activation."}
            )
        self.full_clean()
        super().save(*args, **kwargs)


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    title = models.CharField(max_length=120, default="Untitled task")
    priority = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1, message="priority must be greater than 0.")]
    )
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "tasks"
        ordering = ["priority", "id"]
        indexes = [
            models.Index(fields=["is_completed"]),
            models.Index(fields=["priority"]),
            models.Index(fields=["mission", "priority", "is_completed"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(priority__gt=0),
                name="task_priority_positive",
            ),
        ]

    def __str__(self) -> str:
        return f"Task {self.pk} ({self.mission_id})"

    def clean(self):
        if self.is_completed and self.mission.status not in (
            MissionStatus.ACTIVE,
            MissionStatus.COMPLETED,
        ):
            raise ValidationError(
                {"is_completed": "Completed tasks must belong to active or completed missions."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class MissionParticipation(models.Model):
    mission = models.ForeignKey(
        Mission,
        on_delete=models.CASCADE,
        related_name="participations",
    )
    agent_id = models.UUIDField()
    role = models.CharField(
        max_length=20,
        choices=MissionRole.choices,
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mission_participations"
        ordering = ["-assigned_at"]
        indexes = [
            models.Index(fields=["agent_id"]),
            models.Index(fields=["assigned_at"]),
            models.Index(fields=["mission", "role"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["mission", "agent_id"],
                name="unique_mission_agent",
            ),
        ]

    def get_agent(self):
        from robot_app.models import Robot
        from drone_app.models import Drone

        return Robot.objects.filter(id=self.agent_id).first() or Drone.objects.filter(
            id=self.agent_id
        ).first()

    def clean(self):
        if not self.get_agent():
            raise ValidationError({"agent_id": "agent_id must exist in Robot or Drone."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


def _telemetry_schema_validator(value):
    if not isinstance(value, dict):
        raise ValidationError("Telemetry data must be a JSON object.")
    required = {"location", "velocity", "orientation", "sensors"}
    missing = required - set(value.keys())
    if missing:
        raise ValidationError(f"Telemetry data missing keys: {', '.join(sorted(missing))}.")


class TelemetryRecord(models.Model):
    agent_id = models.UUIDField()
    timestamp = models.DateTimeField()
    data = models.JSONField(validators=[_telemetry_schema_validator])

    class Meta:
        db_table = "telemetry_records"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["timestamp"]),
            models.Index(fields=["agent_id", "-timestamp"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["agent_id", "timestamp"],
                name="unique_telemetry_agent_timestamp",
            ),
        ]

    def get_agent(self):
        from robot_app.models import Robot
        from drone_app.models import Drone

        return Robot.objects.filter(id=self.agent_id).first() or Drone.objects.filter(
            id=self.agent_id
        ).first()

    def clean(self):
        if not self.get_agent():
            raise ValidationError({"agent_id": "agent_id must exist in Robot or Drone."})
