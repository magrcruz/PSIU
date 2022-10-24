from django.db import models
from datetime import datetime
import uuid

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)