from django.urls import path
from . import views

app_name = 'psiuChat'
urlpatterns = [
    path('', views.chatHome, name='chatHome'),
    path('<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
]