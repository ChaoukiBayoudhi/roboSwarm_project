from rest_framework import viewsets
from rest_framework.response import Response
from .models import Robot
from .serializers import RobotSerializer
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q

class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
    #request is the http request object
    #it contains the header and body.
    #the hearder contains the metadata of the request.
    #like the method, the url, the content type, the headers, the status code, etc.
    #the body contains the data of the request.
    #1st case : value as path parameter
    #to call the endpoint:
    #http://127.0.0.1:8000/api/robots/speed_max/50 
    # --> here 50 is the speed_seuil value
    # (?P<speed_seuil>\d+) is a regular expression to match the speed_seuil value
    # \d+ means one or more digits
    #?P<speed_seuil> is the name of the path parameter
    # so the url_path will be http://127.0.0.1:8002/api/robots/speed_max/50
    @action(detail=False, methods=['GET'],url_path='speed/(?P<speed_seuil>\d+)')
    def get_robots_speed_max(self, request, speed_seuil):
        #chech the validity of the speed_seuil
        if float(speed_seuil) <= 0:
            return Response(f"Invalid speed_seuil value: {speed_seuil}", 
            status=status.HTTP_400_BAD_REQUEST)
        #get the robots with speed greater than or equal to the speed_seuil
        robots = Robot.objects.filter(max_speed__gte=float(speed_seuil))
        if not robots.exists():
            return Response(f"No robots found with speed greater than or equal to the {speed_seuil}", 
            status=status.HTTP_204_NO_CONTENT)
        #serialize the robots
        #many=True because we are serializing multiple robots
        result = RobotSerializer(robots, many=True)
        #return the serialized robots
        return Response(result.data)

    #2nd case : value as query parameter
    #to call the endpoint:
    #http://127.0.0.1:8002/api/robots/battery_level?level1=50&level2=70
    #to get the 2 values from the query parameters, we use the request.query_params.get() method
    #request.query_params is a dictionary of the query parameters
    #for example level1=request.query_params.get('level1') will return the value of the level1 query parameter
    #or level1=request.query_params['level1']
    #so the url_path will be http://127.0.0.1:8002/api/robots/battery_level?level1=50&level2=70
    @action(detail=False, methods=['GET'],url_path='battery_level')
    def get_robots_battery_level(self, request):
        try:
            if 'level1' not in request.query_params or 'level2' not in request.query_params.keys():
                return Response(f"Invalid query parameters: {request.query_params}", 
                status=status.HTTP_400_BAD_REQUEST)
            #get the level1 and level2 from the query parameters
            level1 = int(request.query_params['level1'])
            level2 = int(request.query_params['level2'])
            #check the validity of the level1 and level2
            if level1 <= 0 or level2 <= 0:
                return Response(f"Invalid level1 or level2 value: {level1} or {level2}", 
                status=status.HTTP_400_BAD_REQUEST)
            #get the robots with battery level greater than or equal to the level1 and less than or equal to the level2
            #robots = Robot.objects.filter(battery_level__gte=level1, battery_level__lte=level2)
            #or
            #robots=Robot.objects.filter(Q(battery_level__gte=level1) & Q(battery_level__lte=level2))
            #or using range
            robots=Robot.objects.filter(battery_level__range=(level1, level2))
            return Response(RobotSerializer(robots, many=True).data,status.HTTP_200_OK)
        except Exception as e:
            return Response(f"Error: {e}", status.HTTP_400_BAD_REQUEST)