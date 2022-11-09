from django.urls import path
from . import views

app_name = 'psiuAmigos'
urlpatterns = [
    path('', views.index, name='index'),
    path('todos', views.todos, name='todos'),
    path('pendentes', views.pendentes, name='pendentes'),
    path('agregar', views.agregar, name='agregar'),
    path('recente', views.recente, name='recente'),
    path('aceitar/<id>', views.aceitar, name='aceitar'),
]