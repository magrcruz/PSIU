from curses import keyname
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from psiu.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from datetime import datetime
from .forms import caronaFilter, newParticipante

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect(reverse('psiu:login'))

def main(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect(reverse('psiu:login'))

def user_info(request):
    return render(request, 'psiu/user_info.html')

def getTestPerfil():
    fakePerfil = {
        "id":1,
        "telefone" :"(21) 99999-9999",
        "nomeUser":"Ana Luiza",
        "instagram":"@instagram",
        "direcao":"Av. Nossa Senhora 545 - Copacabana",
        "image":"https://cdn.discordapp.com/attachments/1004623388758777966/1019399649100050512/unknown.png",
    }
    return fakePerfil

def filtrar_carona(request, carona_list):
    carona = Carona()

    # there is a better way to do this with forms.py
    form = caronaFilter(request.POST)
    if form.is_valid():
        fields = carona.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    #carona_list = carona_list.filter(criador__startswith=form.cleaned_data["criador"])
    carona_list = carona_list.filter(nomeCarona__startswith=form.cleaned_data["nomeCarona"]or"")
    carona_list = carona_list.filter(localSaida__startswith=form.cleaned_data["localSaida"]or"")
    carona_list = carona_list.filter(localChegada__startswith=form.cleaned_data["localChegada"]or"")
    #carona_list = carona_list.filter(dataHora__startswith=str(datetime.strptime(form.cleaned_data['dataHora'], '%Y-%m-%dT%H:%M'))or"")
    carona_list = carona_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    carona_list = carona_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")

    return carona_list

def carona(request):
    carona_list = Carona.objects.all().values() #to update with filters
    fitro_form = caronaFilter()
    if request.method == "GET":
        for carona in carona_list:
            if 'criador' in carona and carona['criador']!="NULL":
                name = Perfil.objects.get(pk=carona_list['criador'])
                if name:
                    carona['nomeUser'] = name
                continue
            carona['nomeUser'] = "User not found"

    elif request.method == "POST":
        carona_list = filtrar_carona(request,carona_list)

    return render(request, 'psiu/carona.html',{'title':'Carona', 'carona_list':carona_list,'fitro_form':fitro_form})

def criar_carona(request):
    print(request)
    if request.method == "GET":
        carona_temp = None
        return render(request, 'psiu/criar_carona.html', {'carona_temp':carona_temp})

    elif request.method == "POST":
        carona = Carona()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = carona.get_readonly_fields(request)
        content = {} 
        for field in fields:
            if field in form:
                content[field] = form.get(field)

        print(content['dataHora'])#2022-10-06T22:06

        #content['criador_id'] = 
        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')

        carona = Carona(**content)
        carona.save()

        return redirect(reverse('psiu:carona'))

def view_carona(request, id):
    carona = Carona.objects.get(pk = id)
    criador = getTestPerfil()
    try:
        criador = Perfil.objects.get(pk = carona.criador)
    except:
        print("Criador not found")
    return render(request, 'psiu/info_carona.html',{'carona':carona,'contato':criador})

# GRUPO DE ESTUDOS
def info_estudos(request, id):
    formnewParticipante = newParticipante()
    if request.method == "GET":
        print("Estudos")

    if request.method == "POST":
        form = request.POST.dict()
        content = {
            'id_participante':User.objects.get(pk = form.get('id_participante')),
            'id_grupo':Estudos.objects.get(pk = id),
            'rol':form.get('rol')
        }
        estudos = ParticipacaoGrupoEstudos(**content)
        #carona.add_to_class('dataHora', content['dataHora'])
        estudos.save()

    grupo = Estudos.objects.get(pk = id)
    participantes = list(ParticipacaoGrupoEstudos.objects.all().values().filter(id_grupo=id).values())
    #ParticipacaoGrupoEstudos.objects.get(id_grupo = id)
    criador = getTestPerfil()

    return render(request, 'psiu/info_estudos.html',{'grupo':grupo,'contato':criador, 'participantes':participantes,'form':formnewParticipante})

def criar_estudos(request):
    if request.method == "GET":
        return render(request, 'psiu/criar_estudos.html', {})

    elif request.method == "POST":
        estudos = Estudos()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = estudos.get_readonly_fields(request)
        content = {} 
        for field in fields:
            if field in form:
                content[field] = form.get(field)
        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')

        try:
            content['criador_id'] = request.user["perfil"]
        except:
            content['criador_id'] = 1#Fix

        estudos = Estudos(**content)
        estudos.save()

        return redirect(reverse('psiu:grupo_estudos'))

def filtrar_estudos(request, estudos_list):
    estudos = Estudos()

    # there is a better way to do this with forms.py
    form = estudosFilter(request.POST)
    if form.is_valid():
        fields = estudos.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    estudos_list = estudos_list.filter(materia__startswith=form.cleaned_data["materia"]or"")
    estudos_list = estudos_list.filter(local__startswith=form.cleaned_data["local"]or"")
    #estudos_list = estudos_list.filter(dataHora__startswith=str(datetime.strptime(form.cleaned_data['dataHora'], '%Y-%m-%dT%H:%M'))or"")
    estudos_list = estudos_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    estudos_list = estudos_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")

    return estudos_list

def grupo_estudos(request):
    grupo_de_estudos = Estudos.objects.all().values() #to update with filters

    print(grupo_de_estudos.values())
    fitro_form = estudosFilter()
    if request.method == "GET":
        for grupo in grupo_de_estudos:
            if 'criador' in grupo and grupo['criador']!="NULL":
                name = Perfil.objects.get(pk=grupo['criador'])
                if name:
                    grupo['nomeUser'] = name
                continue
            grupo['nomeUser'] = "User not found"

    elif request.method == "POST":
       #Filtrar grupo de estudos
        grupo_de_estudos = filtrar_estudos(request,grupo_de_estudos)

    return render(request, 'psiu/estudos.html',{'title':'Grupo de estudos','grupo_estudos':grupo_de_estudos,'fitro_form':fitro_form})


def extracurriculares(request):
    return render(request, 'base.html',{'title':'Actividades extracurriculares'})
def ligas_academicas(request):
    return render(request, 'base.html',{'title':'Ligas Academicas'})
def conhecer_pessoas(request):
    return render(request, 'base.html',{'title':'Conhecer Pessoas'})

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        profile_form = PerfilForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            login(request, user)
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "Registration successful." )
            return redirect("home")

        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    profile_form = PerfilForm()
    return render (request, "psiu/criar.html", {"criar_form":form, 'profile_form': profile_form})

def info_perfil(request, id):
    return render(request, 'base.html',{'title':'Perfil'})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "psiu/login.html", {"login_form":form})



def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('psiu:login'))

def modificar_request(request):
    if request.method == "POST":
        form = ModificarPerfilForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect(reverse('psiu:user_info'))
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = ModificarPerfilForm()

    return render(request, "psiu/modificar.html", {"form":form})
