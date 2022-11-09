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
    path('criar/', views.register_request, name='criar'),
    path('criar_perfil/',views.perfil_request, name='criar_perfil'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('modificar/', views.modificar_request, name='modificar'),
    path('salas/', views.salas, name='Sala de chat'),
    path('ligas_oficiais/', views.ligas_oficiais, name='ligas_oficiais'),
    path('ligas_nao_oficiais/', views.ligas_nao_oficiais, name='ligas_nao_oficiais'),
    path('modificar_perfil/', views.modificar_perfil, name='modificar_perfil'),

    #criar
    path('criar_carona/',views.criar_carona, name='criar_carona'),
    path('criar_estudos/',views.criar_estudos, name='criar_estudos'),
    #path('criar_pessoas/',views.criar_pessoas, name='criar_pessoas'),
    path('criar_ligas/',views.criar_ligas, name='criar_ligas'),
    path('criar_extracurricular/',views.criar_extracurricular, name='criar_extracurricular'),

    #views
    path('view_carona/<id>', views.view_carona, name='view_carona'),
    path('info_estudos/<id>', views.info_estudos, name='info_estudos'),
    path('info_perfil/<id>', views.info_perfil, name='info_perfil'),
    path('info_extracurricular/<id>', views.info_extracurricular, name='info_extracurricular'),
    path('info_ligas_nao_oficiais/<id>', views.info_ligas_nao_oficiais, name='info_ligas_nao_oficiais'),
]
