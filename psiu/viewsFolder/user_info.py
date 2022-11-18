from .views_common import *

def user_info(request):
    participanteEstudos = Estudos.objects.filter(participacaogrupoestudos__id_participante=request.user)

    return render(request, 'psiu/user_info.html', {'participanteEstudos':participanteEstudos})