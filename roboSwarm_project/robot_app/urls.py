from rest_framework.routers import DefaultRouter
from .views import RobotViewSet
router=DefaultRouter()
router.register(r'robot',RobotViewSet)
urlpatterns=router.urls