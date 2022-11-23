from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from amigos.models import *
from psiu.models import *
from psiu.urls import *
import amigos
from datetime import datetime  

def index(request):
    return redirect(reverse("amigos:todos"))

meusAmigos = [
        {"nome":"Bob", "descricao":"Bob is cool"},
        {"nome":"Rick", "descricao":"Rick is not cool"},
    ]

def recente(request):
    return render(request,"amigos/recente.html", {"disableSearch":True})

def todos(request):
    userId = request.user.id
    meusAmigos = Amizade.objects.all().filter(amigo1 = userId) | Amizade.objects.all().filter(amigo2 = userId)
    amigos = []
    for amizade in meusAmigos:
        #Check if it is not the user
        amigo = Amizade._meta.get_field("amigo1").value_from_object(amizade)[0]
        if amigo == userId:
            amigo = Amizade._meta.get_field("amigo2").value_from_object(amizade)[0]
        
        perfilAmigo = Perfil.objects.filter(user=amigo)
       
        #img=amigo.img nome=amigo.nome descricao=amigo.descricao link1="link" link2="link"
        amigos.append(perfilAmigo.__dict__ |{
            "nome": getattr(amigo,'username')
        })
        #print(amigos[-1])
    #return render(request,"base.html")
    return render(request,"amigos/todos.html", {"amigos": amigos,"disableSearch":False})

def pendentes(request):
    userId = request.user.id
    minhasSolicitudes = Solicitude.objects.filter(user2 = userId)
    amigos = []
    for amizade in minhasSolicitudes:
        #Check if it is not the user
        amigo = Solicitude._meta.get_field("user1").value_from_object(amizade)
        if not amigo: break
        amigo = amigo[0]
        perfilAmigo = Perfil.objects.filter(user=amigo)
       
        #img=amigo.img nome=amigo.nome descricao=amigo.descricao link1="link" link2="link"
        amigos.append(perfilAmigo.__dict__ |{
            "solicitude_id": getattr(amizade,"pk"),
            "nome": getattr(amigo,'username')
        })
    #return render(request,"base.html")
    return render(request,"amigos/pendentes.html", {"amigos": amigos,"disableSearch":True})

def agregar(request):
    #return render(request,"base.html")
    if request.method == 'GET':
        print('get')
    elif request.method == 'POST':
        print('post')
        novaSolicitude = Solicitude.objects.create()
        form = request.POST.dict()
        novaSolicitude.user1.add(request.user.id)
        novaSolicitude.user2.add(form.get('codigo'))
        return render(request,"amigos/agregar.html",{"disableSearch":True,'userId':request.user.id,'alerta':"A solicitude foi enviada com suceso"})
    return render(request,"amigos/agregar.html",{"disableSearch":True,'userId':request.user.id})

def aceitar(request, id):
    
    solicitude = Solicitude.objects.filter(pk = id)
    if solicitude: solicitude=solicitude[0]
    aux =  Solicitude._meta.get_field("user1").value_from_object(solicitude)[0].__dict__
    solicitude.delete()

    idUser = aux["id"]

    print("Solicitud encontrada", idUser)
    amizade = Amizade.objects.create()

    amizade.amigo1.add(idUser)
    amizade.amigo2.add(request.user.id)

    amizade.save()
    
    return redirect(reverse('amigos:pendentes'))

nResults = 20
def get_friends_info(id):
    carona = Carona.objects.all()[:nResults].order_by("dataModificicao")
    lastDate = carona[-1]["dataModificicao"]
    
    estudos = Estudos.objects.exclude(dataModificicao__lt=lastDate)[:nResults].order_by("dataModificicao")
    if estudos[-1]["dataModificicao"]<lastDate:
        lastDate = estudos[-1]["dataModificicao"]
    
    extra = Extra.objects.exclude(dataModificicao__lt=lastDate)[:nResults].order_by("dataModificicao")
    if extra[-1]["dataModificicao"]<lastDate:
        lastDate = extra[-1]["dataModificicao"]
    
    ligas = Ligas.objects.exclude(dataModificicao__lt=lastDate)[:nResults].order_by("dataModificicao")
    if ligas[-1]["dataModificicao"]<lastDate:
        lastDate = Ligas[-1]["dataModificicao"]
    
    perfil = Perfil.objects.exclude(dataModificicao__lt=lastDate)[:nResults].order_by("dataModificicao")
    if perfil[-1]["dataModificicao"]<lastDate:
        lastDate = perfil[-1]["dataModificicao"]
    
    conhecer = Conhecer.objects.exclude(dataModificicao__lt=lastDate)[:nResults].order_by("dataModificicao")
    if conhecer[-1]["dataModificicao"]<lastDate:
        lastDate = conhecer[-1]["dataModificicao"]

    participacaoGrupoEstudos = ParticipacaoGrupoEstudos.objects.exclude(dataModificicao__lt=lastDate)[:nResults].order_by("dataModificicao")
    if participacaoGrupoEstudos[-1]["dataModificicao"]<lastDate:
        lastDate = participacaoGrupoEstudos[-1]["dataModificicao"]

    for i in carona: