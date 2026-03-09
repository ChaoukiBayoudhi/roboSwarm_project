from django.db import models
class MissionStatus(models.TextChoices):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'

class RobotStatus(models.TextChoices):
    IDLE = 'idle'
    MOVING = 'moving'
    MANIPULATING = 'manipulating'
    RECHARGING = 'recharging'
    MAINTENANCE = 'maintenance'
    ERROR = 'error'
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    OFFLINE = 'offline'
    ONLINE = 'online'


class TaskStatus(models.TextChoices):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'