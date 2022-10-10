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
from psiu.carona_view import *
from psiu.estudos_views import *
from psiu.extracurriculares_views import *

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

def extracurriculares(request):
    return render(request, 'psiu/extracurriculares.html', {})


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
        form = ModificarPerfilForm(request.POST, request.FILES, request.user)
        if form.is_valid():
            form.save()
        return redirect(reverse('psiu:user_info'))
    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = ModificarPerfilForm(request.user)

    return render(request, "psiu/modificar.html", {"form":form})
