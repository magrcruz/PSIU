from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponse

from psiu.models import Carona
#from .forms import CriarUsuarioForm

# Create your views here.
def home(request):
    return render(request, 'home.html')
def main(request):
    return render(request, 'home.html')
def user_info(request):
    return render(request, 'psiu/user_info.html')

def criar(request):
#    context ={}
#    form = CriarUsuarioForm(request.POST or None, request.FILES or None)
#    if form.is_valid():
#        form.save()
# 
#    context['form']= form
    return render(request, 'psiu/criar.html', {'title':'Criar'})


def carona(request):
    carona_list = [{'title':'titleCarona'},{'title':'titleCarona2'}]
    return render(request, 'psiu/carona.html',{'title':'Carona', 'carona_list':carona_list})

def criar_carona(request):
    print(request)
    if request.method == "GET":
        carona_temp = None
        return render(request, 'psiu/criar_carona.html', {'carona_temp':carona_temp})

    elif request.method == "POST":
        
        carona = Carona()
        carona.save()
        print(request.POST)
        #carona.add_to_class()
        #carona.save()
        return redirect(reverse('psiu:carona'))
        
    

def grupo_estudos(request):
    return render(request, 'base.html',{'title':'Grupo de estudos'})
def extracurriculares(request):
    return render(request, 'base.html',{'title':'Actividades extracurriculares'})
def ligas_academicas(request):
    return render(request, 'base.html',{'title':'Ligas Academicas'})
def conhecer_pessoas(request):
    return render(request, 'base.html',{'title':'Conhecer Pessoas'})



