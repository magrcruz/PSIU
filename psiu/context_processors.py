from .models import Perfil, Atividade
from django.utils import timezone

def perfilDarkMode(request):
    f = open("ligasOficiais.txt", "r", encoding="utf-8")
    lines = f.readlines()

    for line in lines:
        line = line.split(',')
        if (Atividade.objects.filter(tipo='liga_oficial',materia=line[0],nome=line[1],atividade=line[2]).exists() == False):
            atividade = Atividade(materia=line[0],tipo='liga_oficial',nome=line[1],atividade=line[2],vagas=line[3])
            atividade.save()
    f.close()

    if request.user.is_authenticated:
        usuario = request.user

        try:
            Perfil.objects.get(user=usuario)
        except Perfil.DoesNotExist:
            return {}

        isDarkMode = usuario.perfil.darkMode
        isMiopiaMode = usuario.perfil.miopiaMode
        return {'isDarkMode': isDarkMode, 'isMiopiaMode': isMiopiaMode}
    return {}