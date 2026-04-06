from django.urls import include, path
from rest_framework.routers import DefaultRouter

from drone_app.views import DroneViewSet
from mission_app.views import (
    MissionViewSet,
    MissionParticipationViewSet,
    TaskViewSet,
    TechnicalSpecificationViewSet,
    TelemetryRecordViewSet,
)
from robot_app.views import RobotViewSet

router = DefaultRouter()
router.register(r"robots", RobotViewSet, basename="robot")
router.register(r"drones", DroneViewSet, basename="drone")
router.register(
    r"technical-specifications",
    TechnicalSpecificationViewSet,
    basename="technical-specification",
)
router.register(r"missions", MissionViewSet, basename="mission")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(
    r"mission-participations",
    MissionParticipationViewSet,
    basename="mission-participation",
)
router.register(r"telemetry-records", TelemetryRecordViewSet, basename="telemetry-record")

urlpatterns = [path("", include(router.urls))]
