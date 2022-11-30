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
from .viewsFolder.user_info import *
from .viewsFolder.views_common import *
from .viewsFolder.login import *
from .viewsFolder.darkModeMiopia import *
from .viewsFolder.atividade_views import *

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

def modificar_perfil(request):
    return render(request, 'psiu/modificar_perfil.html')

def modificar_atividade(request):
    return render(request, 'psiu/modificar_atividade.html')

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration successful.")
            return redirect(reverse('psiu:criar_perfil'))

        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request, "psiu/criar.html", {"criar_form":form})

def perfil_request(request):
    if request.method == "POST":
        profile_form = PerfilForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect("home")

        messages.error(request, "Unsuccessful registration. Invalid information.")
    profile_form = PerfilForm()
    return render (request, "psiu/criar_perfil.html", {'profile_form': profile_form})

def logout_request(request):
    
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('psiu:login'))

def modificar_request(request):
    if request.method == "POST":
        form = ModificarPerfilForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.save()
        return redirect(reverse('psiu:user_info'))
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = ModificarPerfilForm(request.user)

    return render(request, "psiu/modificar.html", {"form":form})

def update_user_social_data(strategy, *args, **kwargs):
  response = kwargs['response']
  backend = kwargs['backend']
  user = kwargs['user']

  if response['fotoPerfil']:
    url = response['fotoPerfil']
    userProfile_obj = UserProfile()
    userProfile_obj.user = user
    userProfile_obj.picture = url
    userProfile_obj.save()

@login_required
def salas(request):
    salas = Sala.objects.all()
    return render(request, 'psiu/salas.html', {'salas': salas})

def ajuda(request):
    return render(request, 'psiu/ajuda.html')

def ligas_oficiais(request):
    return render(request, 'psiu/ligas_oficiais.html',{'title':'Ligas Oficiais'})

def ligas_academicas(request):
    return render(request, 'psiu/ligas_academicas.html',{'title':'Ligas Academicas'})