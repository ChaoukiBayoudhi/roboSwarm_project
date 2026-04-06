from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from .views import MissionViewSet,TaskViewSet,MissionParticipationViewSet

router=DefaultRouter()
router.register(r'mission',MissionViewSet)
router.register(r'participation',MissionParticipationViewSet)
router.register(r'task',TaskViewSet)

urlpatterns=router.urls