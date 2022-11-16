from .models import Perfil

def perfilDarkMode(request):
    if request.user.is_authenticated:
        usuario = request.user

        try:
            perfilUser = Perfil.objects.get(user=usuario)
        except Perfil.DoesNotExist:
            perfilUser = None
        if (perfilUser == None):
            return {}

        isDarkMode = usuario.perfil.darkMode
        return {'isDarkMode': isDarkMode}
    return {}