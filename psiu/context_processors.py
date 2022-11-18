from .models import Perfil

def perfilDarkMode(request):
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