from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from amigos.models import *

import amigos

def index(request):
    return redirect(reverse("amigos:todos"))

meusAmigos = [
        {"nome":"Bob", "descricao":"Bob is cool"},
        {"nome":"Rick", "descricao":"Rick is not cool"},
    ]

def recente(request):
    return render(request,"amigos/recente.html", {"disableSearch":True})

def todos(request):
    id = request.user.id
    #meusAmigos = Amizade.objects.get(amigo1 = id) #| Amizade.objects.get(amigo2 = id)

    #return render(request,"base.html")
    return render(request,"amigos/todos.html", {"amigos": meusAmigos,"disableSearch":False})

def pendentes(request):
    #return render(request,"base.html")
    return render(request,"amigos/pendentes.html", {"amigos": meusAmigos,"disableSearch":True})

def agregar(request):
    #return render(request,"base.html")
    return render(request,"amigos/agregar.html",{"disableSearch":True})
