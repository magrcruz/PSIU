from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponse

from psiu.models import *
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



