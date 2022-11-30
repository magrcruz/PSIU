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
    atividades = get_friends_info(request.user.id)
    
    return render(request,"amigos/recente.html", {"disableSearch":True,"atividades":atividades})

def todos(request):
    userId = request.user.id
    meusAmigos = Amizade.objects.all().filter(amigo1 = userId) | Amizade.objects.all().filter(amigo2 = userId)
    amigos = []
    for amizade in meusAmigos:
        #Check if it is not the user
        amigo = Amizade._meta.get_field("amigo1").value_from_object(amizade)[0]
        if amigo != userId:
            amigo = Amizade._meta.get_field("amigo2").value_from_object(amizade)[0]
        
        perfilAmigo = Perfil.objects.filter(user=amigo)
       
        #img=amigo.img nome=amigo.nome descricao=amigo.descricao link1="link" link2="link"
        sala = getattr(amizade,'sala')
        if sala: sala = sala.name

        amigos.append(perfilAmigo.__dict__ |{
            "nome": getattr(amigo,'username'),
            "bio": getattr(amigo.perfil,'bio'),
            "sala":sala
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

    idUser = aux["id"]

    print("Solicitud encontrada", idUser)
    sala = Room.objects.create()

    amizade = Amizade.objects.create(sala=sala)

    amizade.amigo1.add(idUser)
    amizade.amigo2.add(request.user.id)

    amizade.save()
    solicitude.delete()

    return redirect(reverse('amigos:pendentes'))

'''
STEPS 
For each friend:
    get the 5 most recents activities(
        for each kind of activity get 5
        #for 1 to 5 compare all kinds to get the most recent one
        mix kinds and sort by date
        extract the top 5
    )
    mix kinds and sort by date
    extract the top 5
'''

def getUserActivity(user):
    activitiesObjects = Atividade.objects.filter(criador_id = user.id)[:5]
    userActivities = []
    for j in activitiesObjects:
        userActivities.append(
            {
                "tipo": getattr(j,'tipo'),
                "user":user.username,
                "data":getattr(j,'dataModificacao'),
            }
        )
 
    return sorted(userActivities,key=lambda x:x["data"],reverse=True)[:5]
#datetime.datetime

nResults = 20
def get_friends_info(id):
    userId = id
    meusAmigos = Amizade.objects.all().filter(amigo1 = userId) | Amizade.objects.all().filter(amigo2 = userId)
    amigos = []
    atividades = []
    for amizade in meusAmigos:
        #Check if it is not the user
        amigo = Amizade._meta.get_field("amigo1").value_from_object(amizade)[0]
        if amigo != userId:
            amigo = Amizade._meta.get_field("amigo2").value_from_object(amizade)[0]
        amigos.append(amigo)
    for i in amigos:
        atividades.extend(getUserActivity(i))
    
    return sorted(atividades,key=lambda x:x["data"],reverse=True)[:20]