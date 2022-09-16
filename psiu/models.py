from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

#class Usuario(models.Model):
#  nome = models.CharField(max_length=30)
#  sobrenome = models.CharField(max_length=30)
#  email = models.EmailField(max_length = 254)
#  fotoPerfl = models.ImageField(upload_to='fotos')

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()



#Cada classe abaixo é uma "many to one relationship" com um usuario
#Isso é, um usuario pode ter diversas caronas, mas a carona só pode ter um "criador"
class Carona(models.Model):
  criador = models.ForeignKey(User, on_delete=models.CASCADE)
  localSaida = models.CharField(max_length=30)
  localChegada = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField()
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
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