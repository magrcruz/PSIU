from .models import Perfil

def perfilDarkMode(request):
    if request.user.is_authenticated:
        usuario = request.user
        isDarkMode = usuario.perfil.darkMode
        return {'isDarkMode': isDarkMode}
    return {}