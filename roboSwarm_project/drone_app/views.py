from rest_framework import viewsets

from .models import Drone
from .serializers import DroneSerializer


class DroneViewSet(viewsets.ModelViewSet):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
