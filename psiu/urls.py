from django.urls import path
from . import views

app_name = 'psiu'
urlpatterns = [
    path('', views.home, name='main'),
    path('user_info/', views.user_info, name='user_info'),
    path('carona/', views.carona, name='carona'),
    path('grupo_estudos/', views.grupo_estudos, name='grupo_estudos'),
    path('extracurriculares/', views.extracurriculares, name='extracurriculares'),
    path('ligas_academicas/', views.ligas_academicas, name='ligas_academicas'),
    path('conhecer_pessoas/', views.conhecer_pessoas, name='conhecer_pessoas'),
    path('criar/', views.criar, name='criar'),
]