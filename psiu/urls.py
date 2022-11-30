from django.urls import path
from . import views

app_name = 'psiu'
urlpatterns = [
    path('', views.home, name='main'),
    path('user_info/<id>', views.user_info, name='user_info'),
    path('carona/', views.listaAtividades, name='carona'),
    path('grupo_estudos/', views.listaAtividades, name='grupo_estudos'),
    path('extracurriculares/', views.listaAtividades, name='extracurriculares'),
    path('ligas_academicas/', views.ligas_academicas, name='ligas_academicas'),
    path('conhecer_pessoas/', views.listaAtividades, name='conhecer_pessoas'),
    path('criar/', views.register_request, name='criar'),
    path('criar_perfil/',views.perfil_request, name='criar_perfil'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('modificar/', views.modificar_request, name='modificar'),
    path('salas/', views.salas, name='Sala de chat'),
    path('ligas_oficiais/', views.listaAtividades, name='ligas_oficiais'),
    path('modificar_perfil/', views.modificar_perfil, name='modificar_perfil'),
    path('modificar_atividade/', views.modificar_atividade, name='modificar_atividade'),
    path('ajuda/', views.ajuda, name='ajuda'),

    path('carona/', views.listaAtividades, name='carona'),
    path('grupo_estudos/', views.listaAtividades, name='grupo_estudos'),
    path('extracurriculares/', views.listaAtividades, name='extracurriculares'),
    path('ligas/', views.listaAtividades, name='ligas'),
    path('conhecer_pessoas/', views.listaAtividades, name='conhecer_pessoas'),

    #criar
    path('criar_carona/',views.criar_atividade, name='criar_carona'),
    path('criar_estudos/',views.criar_atividade, name='criar_estudos'),
    path('criar_conhecer/',views.criar_atividade, name='criar_conhecer'),
    path('criar_liga/',views.criar_atividade, name='criar_ligas'),
    path('criar_extracurricular/',views.criar_atividade, name='criar_extracurricular'),
    path('darkMode/', views.darkMode_request, name='darkMode'),
    path('miopiaMode/', views.miopiaMode_request, name='miopiaMode'),
    path('corMode/', views.corMode_request, name='corMode'),
    
    #deletar
    path('apagar_carona/<id>',views.apagar_atividade, name='apagar_carona'),
    path('apagar_estudos/<id>',views.apagar_atividade, name='apagar_estudos'),
    path('apagar_extracurricular/<id>',views.apagar_atividade, name='apagar_extracurricular'),
    path('apagar_conhecer/<id>',views.apagar_atividade, name='apagar_conhecer'),
    path('apagar_liga/<id>',views.apagar_atividade, name='apagar_liga'),

    #participar
    path('participar_carona/<id>',views.participar_atividade, name='participar_carona'),
    path('participar_estudos/<id>',views.participar_atividade, name='participar_estudos'),
    path('participar_extracurricular/<id>',views.participar_atividade, name='participar_extracurricular'),
    path('participar_conhecer/<id>',views.participar_atividade, name='participar_conhecer'),
    path('participar_liga/<id>',views.participar_atividade, name='participar_liga'),
    path('participar_liga_oficial/<id>',views.participar_atividade, name='participar_liga_oficial'),

    #sair
    path('sair_carona/<id>',views.sair_atividade, name='sair_carona'),
    path('sair_estudos/<id>',views.sair_atividade, name='sair_estudos'),
    path('sair_extracurricular/<id>',views.sair_atividade, name='sair_extracurricular'),
    path('sair_conhecer/<id>',views.sair_atividade, name='sair_conhecer'),
    path('sair_liga/<id>',views.sair_atividade, name='sair_liga'),
    path('sair_liga_oficial/<id>',views.sair_atividade, name='sair_liga_oficial'),

    #views
    path('info_carona/<id>', views.info_atividade, name='view_carona'),
    path('info_estudos/<id>', views.info_atividade, name='info_estudos'),
    path('info_extracurricular/<id>', views.info_atividade, name='info_extracurricular'),
    path('info_liga/<id>', views.info_atividade, name='info_liga'),
    path('info_liga_oficial/<id>',views.info_atividade, name='info_liga_oficial'),
    path('info_conhecer/<id>', views.info_atividade, name='info_conhecer'),
]
