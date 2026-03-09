from django.db import models
from django.db.models.fields import timezone
from robot_app.models import Robot
from drone_app.models import Drone
from enumerations.enums import MissionStatus, TaskStatus
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
class TechnicalSpecification(models.Model):
    id = models.AutoField(primary_key=True)
    robot = models.OneToOneField(Robot, on_delete=models.CASCADE, null=True, blank=True)
    drone = models.OneToOneField(Drone, on_delete=models.CASCADE, null=True, blank=True)
    cpu=models.CharField(max_length=100)
    memory_gb=models.PositiveSmallIntegerField(default=0)
    storage_gb=models.PositiveSmallIntegerField(default=0)
    firmware_version=models.CharField(max_length=100)
    class Meta:
        db_table = 'technical_specifications'
        ordering = ['-cpu', '-memory_gb', '-storage_gb', '-firmware_version']
        indexes = [
            models.Index(fields=['cpu']),
            models.Index(fields=['memory_gb']),
            models.Index(fields=['storage_gb']),
            models.Index(fields=['firmware_version']),
        ]
        

class Mission(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100,validators=[MinLengthValidator(7, message='Name must be at least 7 characters long.')])
    description=models.TextField(blank=True)
    start_time=models.DateTimeField(default=timezone.now())
    end_time=models.DateTimeField()
    status=models.CharField(max_length=100, choices=MissionStatus.choices)
    
    class Meta:
        db_table = 'missions'
        ordering = ['-start_time', '-end_time']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['start_time']),
            models.Index(fields=['end_time']),
            models.Index(fields=['status']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name', 'start_time', 'end_time'], name='unique_mission'),
        ]
    def __str__(self)->str:
        return f'{self.name} - {self.start_time} - {self.end_time} - {self.status}'

    #overide the clean method to validate the start_time and end_time
    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError({'start_time': 'Start time must be before end time.'})
        
class Task(models.Model):
    id=models.AutoField(primary_key=True)
    mission=models.ForeignKey(Mission, on_delete=models.CASCADE)
    duration=models.DurationField()
    status=models.CharField(max_length=100, choices=TaskStatus.choices)
    class Meta:
        db_table = 'tasks'
        ordering = ['-duration']
        indexes = [
            models.Index(fields=['duration']),
            models.Index(fields=['status']),
        ]
    #overide the clean method to validate the duration of task compared to the deuration ot the mission
    def clean(self):
        if self.duration > self.mission.end_time - self.mission.start_time:
            raise ValidationError({'duration': 'Duration must be less than or equal to the duration of the mission.'})

        #the sum of the durations of the tasks must be equal to the duration of the mission
        if self.mission.end_time - self.mission.start_time != sum(task.duration for task in self.mission.tasks.all()):
            raise ValidationError({'duration': 'The sum of the durations of the tasks must be equal to the duration of the mission.'})
        

class Agent(models.Model):
    id=models.AutoField(primary_key=True)
    robot=models.OneToOneField(Robot, on_delete=models.CASCADE, null=True, blank=True)
    drone=models.OneToOneField(Drone, on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        db_table = 'agents'
        ordering = ['-robot', '-drone']
        
class Participation(models.Model):
    id=models.AutoField(primary_key=True)
    task=models.ForeignKey(Task, on_delete=models.CASCADE)
    agent=models.ForeignKey(Agent, on_delete=models.CASCADE)
    status=models.CharField(max_length=100)
    class Meta:
        db_table = 'participations'
        ordering = ['-task', '-agent']
        indexes = [
            models.Index(fields=['task']),
            models.Index(fields=['agent']),
            models.Index(fields=['status']),
        ]
        
        
        