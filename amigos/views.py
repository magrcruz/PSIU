from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from amigos.models import *
from psiu.models import Perfil, User
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
    meusAmigos = Amizade.objects.filter(amigo1 = userId) | Amizade.objects.filter(amigo2 = userId)
    amigos = []
    for amizade in meusAmigos:
        #Check if it is not the user
        amigo = Amizade._meta.get_field("amigo1").value_from_object(amizade)[0]
        if amigo != userId:
            amigo = Amizade._meta.get_field("amigo2").value_from_object(amizade)[0]
        
        perfilAmigo = Perfil.objects.get(user=amigo)
       
        #img=amigo.img nome=amigo.nome descricao=amigo.descricao link1="link" link2="link"
        amigos.append(perfilAmigo.__dict__ |{
            "nome": getattr(amigo,'username')
        })
        #print(amigos[-1])
    #return render(request,"base.html")
    return render(request,"amigos/todos.html", {"amigos": amigos,"disableSearch":False})

def pendentes(request):
    userId = request.user.id
    minhasSolicitudes = Solicitude.objects.filter(user1 = userId) | Solicitude.objects.filter(user2 = userId)
    amigos = []
    for amizade in minhasSolicitudes:
        #Check if it is not the user
        amigo = Solicitude._meta.get_field("user1").value_from_object(amizade)[0]
        if amigo != userId:
            amigo = Solicitude._meta.get_field("user2").value_from_object(amizade)[0]
        
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
    return render(request,"amigos/agregar.html",{"disableSearch":True})

def aceitar(request, id):
    
    solicitude = Solicitude.objects.filter(pk = id)[0]
    print(solicitude)
    print("Solicitud encontrada")
    amizade = Amizade.objects.create()
    amizade.setAttr("data",datetime.now)
    print("aqui", amizade)
    amizade.amigo1.add(getattr(solicitude,'user1'))
    amizade.amigo2.add(getattr(solicitude,'user2'))

    amizade.save()
    
    return redirect(reverse('amigos:pendentes'))


