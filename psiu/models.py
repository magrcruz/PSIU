from django.db import models

class Usuario(models.Model):
  usuarioId = models.BigAutoField(primary_key=True)
  nome = models.CharField(max_length=30)
  sobrenome = models.CharField(max_length=30)
  email = models.EmailField(max_length = 254)
  
  def __str__(self):
    return self.usuarioId
  
#Cada classe abaixo é uma "many to one relationship" com um usuario
#Isso é, um usuario pode ter diversas caronas, mas a carona só pode ter um "criador"
class Carona(models.Model):
  caronaId = models.BigAutoField(primary_key=True)
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  localSaida = models.CharField(max_length=30)
  localChegada = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField()
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
  def __str__(self):
    return self.caronaId
  
class Estudos(models.Model):
  estudosId = models.BigAutoField(primary_key=True)
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  materia = models.CharField(max_length=10)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
  def __str__(self):
    return self.estudosId
  
class Extra(models.Model):
  extraId = models.BigAutoField(primary_key=True)
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  atividade = models.CharField(max_length=30)
  local = models.CharField(max_length=30)
  dataHora = models.DateTimeField()
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
  def __str__(self):
    return self.extraId
  
class Conhecer(models.Model):
  conhecerId = models.BigAutoField(primary_key=True)
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  interesses = models.CharField(max_length=30)
  local = models.CharField(max_length=30, blank=True, default='')
  dataHora = models.DateTimeField(blank=True)
  vagas = models.IntegerField(blank=True, default=-1)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
  def __str__(self):
    return self.conhecerId
 
class Ligas(models.Model):
  ligasId = models.BigAutoField(primary_key=True)
  criador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  nomeLiga = models.CharField(max_length=30)
  adicionais = models.CharField(max_length=254, blank=True, default='')
  
  def __str__(self):
    return self.ligasId
