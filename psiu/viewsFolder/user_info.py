from .views_common import *

def user_info(request, id):
    thisUser = User.objects.filter(id=id)
    if thisUser and len(thisUser): thisUser = thisUser[0]
    else: thisUser = request.user
    atividades = {
        'estudos' : Estudos.objects.filter(participacaogrupoestudos__id_participante=id),
        'caronas' : Carona.objects.filter(criador_id=id),
        'extra' : Extra.objects.filter(criador_id=id),
        'ligas' : Ligas.objects.filter(criador_id=id),
        'conhecer' : Conhecer.objects.filter(criador_id=id),
    }
    
    return render(request, 'psiu/user_info.html', {'thisUser':thisUser,'atividades':atividades})