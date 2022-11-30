from .views_common import *

def darkMode_request(request):
    usuario = request.user
    if (usuario.perfil.darkMode):
        usuario.perfil.darkMode = False
        usuario.perfil.save()
    else:
        usuario.perfil.darkMode = True
        usuario.perfil.save()

    return redirect(reverse('psiu:modificar_perfil'))

def miopiaMode_request(request):        
    usuario = request.user
    if (usuario.perfil.miopiaMode):
        usuario.perfil.miopiaMode = False
        usuario.perfil.save()
    else:
        usuario.perfil.miopiaMode = True
        usuario.perfil.save()

    return redirect(reverse('psiu:modificar_perfil'))