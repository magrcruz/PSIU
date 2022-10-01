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
from .forms import caronaFilter

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
    carona_list = carona_list.filter(dataHora__startswith=form.cleaned_data["dataHora"]or"")
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

        #content['criador_id'] = 
        print(request.user)
        #print( content['dataHora'])
        #content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')
        #print( content['dataHora'])

        carona = Carona(**content)
        #carona.add_to_class('dataHora', content['dataHora'])
        carona.save()

        return redirect(reverse('psiu:carona'))

def view_carona(request, id):
    carona = Carona.objects.get(pk = id)
    return render(request, 'psiu/info_carona.html',{'carona':carona})

# GRUPO DE ESTUDOS
def info_estudos(request, id):
    return "algo"

def filtrar_estudos(request, estudos_list):
    return estudos_list

def grupo_estudos(request):
    grupo_de_estudos = Estudos.objects.all().values() #to update with filters
    #fitro_form = caronaFilter()
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
        grupo_de_estudos = filtrar_estudos()

    return render(request, 'psiu/estudos.html',{'title':'Grupo de estudos','grupo_estudos':grupo_de_estudos})

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
