from django.shortcuts import render
from django.http import HttpResponse 

# Create your views here.
def home(request):
    return render(request, 'home.html')
def main(request):
    return render(request, 'home.html')
def user_info(request):
    return render(request, 'psiu/user_info.html')

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
def teste(request):
    if request.method == 'GET':
    context = {'title': 'User Form Page'}
    template = 'films/user_form.html'

    return render(request,
                  template,
                  context)
    elif request.method == 'POST':
        username = request.POST.get('username')
        country = request.POST.get('country')
        request.session['username'] = username
        request.session['country'] = country

        return redirect(reverse('films:user_info'))
