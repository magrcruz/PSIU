from django.shortcuts import render
from django.http import HttpResponse
from .forms import CriarUsuarioForm

# Create your views here.
def home(request):
    return render(request, 'home.html')
def main(request):
    return render(request, 'home.html')
def user_info(request):
    return render(request, 'psiu/user_info.html')

def criar(request):
    context ={}
    form = CriarUsuarioForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
 
    context['form']= form
    return render(request, 'psiu/criar.html', context)


def carona(request):
    return render(request, 'base.html',{'title':'Carona'})
def grupo_estudos(request):
    return render(request, 'base.html',{'title':'Grupo de estudos'})
def extracurriculares(request):
    return render(request, 'base.html',{'title':'Actividades extracurriculares'})
def ligas_academicas(request):
    return render(request, 'base.html',{'title':'Ligas Academicas'})
def conhecer_pessoas(request):
    return render(request, 'base.html',{'title':'Conhecer Pessoas'})