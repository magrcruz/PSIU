from curses import keyname
from django.shortcuts import render, redirect
from django.urls import reverse
from ..forms import *
from django.contrib.auth import login, authenticate
from django.contrib import messages
from psiu.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from datetime import datetime

def getTestPerfil():
    fakePerfil = {
        "id":1,
        "telefone" :"(21) 99999-9999",
        "nomeUser":"Ana Luiza",
        "instagram":"@instagram",
        "direcao":"Av. Nossa Senhora 545 - Copacabana",
        "image":"https://cdn.discordapp.com/attachments/1004623388758777966/1019399649100050512/unknown.png",
    }
    return fakePerfil
class Icon:
    def __init__(self, imgName):
        self.route = 'static/psiu/'+ imgName#
    @property
    def getHtml(self):
        return '''
        <div class="flex-wrapper">
            <div class="tag">
              <img src="%s" alt="">
            </div>
        </div>
        <div class="icon-floor"></div>
        ''' % (self.route)

icones = {
    "carona": Icon("carona.png"),
    "estudos": Icon("estudos.png"),
    "extra": Icon("extra.png"),
    "ligas": Icon("ligas.png"),
    "pessoas": Icon("pessoas.png"),
}
