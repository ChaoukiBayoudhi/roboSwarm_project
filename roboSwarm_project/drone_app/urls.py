from rest_framework.routers import DefaultRouter

from .views import DroneViewSet
router=DefaultRouter()
router.register(r'drone',DroneViewSet)

urlpatterns=router.urls