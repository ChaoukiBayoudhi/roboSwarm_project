from django.db import models
from django.db.models.fields import uuid

# Create your models here.
class Robot(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=100)
    serial_number=models.CharField(max_length=100,unique=True)