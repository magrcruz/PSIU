from .views_common import *

def user_info(request, id):
    atividades = {
        'estudos' : Estudos.objects.filter(participacaogrupoestudos__id_participante=id),
        'caronas' : Carona.objects.filter(criador_id=id),
        'extra' : Extra.objects.filter(criador_id=id),
        'ligas' : Ligas.objects.filter(criador_id=id),
        'conhecer' : Conhecer.objects.filter(criador_id=id),
    }
    
    return render(request, 'psiu/user_info.html', {'atividades':atividades})