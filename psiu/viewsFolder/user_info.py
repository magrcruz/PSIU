from .views_common import *

def user_info(request, id):
    thisUser = User.objects.filter(id=id)
    if thisUser and len(thisUser): thisUser = thisUser[0]
    else: thisUser = request.user
    atividades = {
        'estudos' : Atividade.objects.filter(participacaogrupoestudos__id_participante=id,tipo='estudo'),
        'caronas' : Atividade.objects.filter(criador_id=id,tipo='carona'),
        'extra' : Atividade.objects.filter(criador_id=id,tipo='extra'),
        'ligas' : Atividade.objects.filter(criador_id=id,tipo='liga'),
        'conhecer' : Atividade.objects.filter(criador_id=id,tipo='conhecer'),
    }
    
    return render(request, 'psiu/user_info.html', {'thisUser':thisUser,'atividades':atividades})