from django.db import models


class MissionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    ACTIVE = "active", "Active"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class MissionRole(models.TextChoices):
    LEADER = "leader", "Leader"
    FOLLOWER = "follower", "Follower"
    SCOUT = "scout", "Scout"
    CARRIER = "carrier", "Carrier"
    OBSERVER = "observer", "Observer"
