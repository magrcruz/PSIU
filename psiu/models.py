from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

#Cada classe abaixo é uma "many to one relationship" com um usuario
#Isso é, um usuario pode ter diversas caronas, mas a carona só pode ter um "criador"
class Carona(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  nomeCarona = models.CharField(max_length=254,blank=False,default='Minha carona')
  localSaida = models.CharField(max_length=30,null=True)
  localChegada = models.CharField(max_length=30,null=True)
  dataHora = models.DateTimeField(auto_now_add=True, blank=True)#Just to prove it
  vagas = models.IntegerField(default=4,null=True)
  adicionais = models.CharField(max_length=254, blank=True, default='')

  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]
  
class Estudos(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  materia = models.CharField(max_length=10)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
class Extra(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  atividade = models.CharField(max_length=30)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
class Conhecer(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  interesses = models.CharField(max_length=30)
  local = models.CharField(max_length=30, blank=True, default='')
  dataHora = models.DateTimeField(blank=True)
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
 
class Ligas(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  nomeLiga = models.CharField(max_length=30)
  adicionais = models.CharField(max_length=254, blank=True, default='')


class Perfil(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.CharField(max_length=30)
  fotoPerfil = models.ImageField(upload_to='images/')