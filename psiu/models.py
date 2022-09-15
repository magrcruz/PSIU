from django.db import models

class Usuario(models.Model):
  nome = models.CharField(max_length=30)
  sobrenome = models.CharField(max_length=30)
  email = models.EmailField(max_length = 254)
  
#Cada classe abaixo é uma "many to one relationship" com um usuario
#Isso é, um usuario pode ter diversas caronas, mas a carona só pode ter um "criador"
class Carona(models.Model):
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  localSaida = models.CharField(max_length=30)
  localChegada = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField()
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
class Estudos(models.Model):
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  materia = models.CharField(max_length=10)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
class Extra(models.Model):
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  atividade = models.CharField(max_length=30)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
class Conhecer(models.Model):
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  interesses = models.CharField(max_length=30)
  local = models.CharField(max_length=30, blank=True, default='')
  dataHora = models.DateTimeField(blank=True)
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
 
class Ligas(models.Model):
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  nomeLiga = models.CharField(max_length=30)
  adicionais = models.CharField(max_length=254, blank=True, default='')
