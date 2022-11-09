from email.policy import default
from django.db import models
from psiu.models import User, Perfil
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Amizade(models.Model):
    amigo1 = models.ManyToManyField(User, related_name="amigo1", default = "")
    amigo2 = models.ManyToManyField(User, related_name="amigo2", default = "")
    data = models.DateField()

class Solicitude(models.Model):
    user1 = models.ManyToManyField(User, related_name="user1", default = "")
    user2 = models.ManyToManyField(User, related_name="user2", default = "")
