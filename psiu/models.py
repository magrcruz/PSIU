from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from psiuChat.models import Room

#Cada classe abaixo é uma "many to one relationship" com um usuario
#Isso é, um usuario pode ter diversas caronas, mas a carona só pode ter um "criador"
class Carona(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
  localSaida = models.CharField(max_length=30,null=True, blank=True)
  localChegada = models.CharField(max_length=30,null=True, blank=True)
  dataHora = models.DateTimeField(auto_now_add=False, blank=True)#Just to prove it
  vagas = models.IntegerField(default=4,null=True)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  sala = models.ForeignKey(Room, on_delete=models.CASCADE,default=1)
  
  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]

class Estudos(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
  materia = models.CharField(max_length=10)
  local = models.CharField(max_length=30,blank=True)
  dataHora = models.DateTimeField(blank=True)
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, default='',blank=True)
  sala = models.ForeignKey(Room, on_delete=models.CASCADE,default=1)
  
  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]
  
class ParticipacaoGrupoEstudos(models.Model):
  id_participante = models.ForeignKey(User, on_delete=models.CASCADE)
  id_grupo = models.ForeignKey(Estudos, on_delete=models.CASCADE)
  rol = models.CharField(max_length=30,blank=True)

class Extra(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  atividade = models.CharField(max_length=30)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  sala = models.ForeignKey(Room, on_delete=models.CASCADE,default=1)
  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]
  
class Conhecer(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  interesses = models.CharField(max_length=30)
  local = models.CharField(max_length=30, blank=True, default='')
  dataHora = models.DateTimeField(blank=True)
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  sala = models.ForeignKey(Room, on_delete=models.CASCADE,default=1)
  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]
 
class Ligas(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  nomeLiga = models.CharField(max_length=30)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  sala = models.ForeignKey(Room, on_delete=models.CASCADE,default=1)
  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]

from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try: #to allow authentication through phone number or any other field, modify the below statement
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(email=username).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None


class Perfil(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  bio = models.CharField(max_length=30,default='')
  fotoPerfil = models.ImageField(upload_to='images/',default='images/default.png')
  instagram = models.CharField(max_length=20,default='')
  twitter = models.CharField(max_length=15,default='')

  darkMode = models.BooleanField(default=False)

  def get_readonly_fields(self, request, obj=None):
    return [f.name for f in self._meta.get_fields()]