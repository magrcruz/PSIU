from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import HttpResponse
from psiu.models import *
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def home(request):
    return render(request, 'home.html')
def main(request):
    return render(request, 'home.html')

def user_info(request):
    return render(request, 'psiu/user_info.html')

def carona(request):
    carona_list = Carona.objects.all().values() #to update with filters
    return render(request, 'psiu/carona.html',{'title':'Carona', 'carona_list':carona_list})

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

        carona = Carona(**content)
        carona.save()

        return redirect(reverse('psiu:carona'))


def grupo_estudos(request):
    return render(request, 'base.html',{'title':'Grupo de estudos'})
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