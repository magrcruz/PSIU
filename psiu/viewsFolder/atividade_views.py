from .views_common import *
from django.http import HttpResponseRedirect

# GRUPO DE ESTUDOS
def info_atividade(request, id):
    formnewParticipante = newParticipante()

    if request.method == "POST":
        form = request.POST.dict()
        content = {
            'id_participante':User.objects.get(pk = form.get('id_participante')),
            'id_grupo':Atividade.objects.get(pk = id),
            'rol':form.get('rol')
        }
        atividade = ParticipacaoAtividade(**content)
        atividade.save()

    atividade = Atividade.objects.get(pk = id)
    participantes = list(ParticipacaoAtividade.objects.all().values().filter(id_grupo=id).values())

    isParticipante = False
    for p in participantes:
        perfil = Perfil.objects.get(user_id = p['id_participante_id'])
        if perfil is not None and perfil.fotoPerfil:
            p["image"] = perfil.fotoPerfil#"images/default.png"
        else:
            p["image"] = "images/default.png"

        usuario = User.objects.get(pk = p['id_participante_id'])
        if usuario is not None and usuario.first_name:
            p["nome"] = usuario.first_name
        if (request.user == usuario):
            isParticipante = True

    if (request.user == atividade.criador):
        isCriador = True
    else:
        isCriador = False

    tipoAtividade = pegarTipoAtividade(request)
    context = pegarContext(tipoAtividade)

    context['grupo'] = atividade
    context['participantes'] = participantes
    context['form'] = formnewParticipante
    context['isCriador'] = isCriador
    context['isParticipante'] = isParticipante

    return render(request, 'psiu/info_atividade.html',context)



def criar_atividade(request):
    tipoAtividade = pegarTipoAtividade(request)
    context = pegarContext(tipoAtividade)

    if request.method == "GET":
        return render(request, 'psiu/criar_atividade.html', context)

    elif request.method == "POST":
        atividade = Atividade()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = atividade.get_readonly_fields(request)
        content = {}
        for field in fields:
            if field in form:
                content[field] = form.get(field)
        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')

        new_room = Room.objects.create()
        new_room.save()

        content['criador_id'] = request.user.id
        
        atividade = Atividade(**content, sala=new_room, tipo=tipoAtividade)
        atividade.save()

        participante = ParticipacaoAtividade(id_participante=request.user, id_grupo=atividade, rol="Criador")
        participante.save()

        if (tipoAtividade == 'estudo'):
            return redirect(reverse('psiu:grupo_estudos'))
        if (tipoAtividade == 'carona'):
            return redirect(reverse('psiu:carona'))
        if (tipoAtividade == 'extracurricular'):
                return redirect(reverse('psiu:extracurriculares'))
        if (tipoAtividade == 'conhecer'):
            return redirect(reverse('psiu:conhecer_pessoas'))
        if (tipoAtividade == 'ligas'):
            return redirect(reverse('psiu:liga'))

        return redirect(reverse('home'))

def filtrar_atividade(request, atividade_list,tipoAtividade):
    atividade = Atividade()

    form = request.POST.dict()
    fields = atividade.get_readonly_fields(request)
    content = {} 
    for field in fields:
        if field in form:
            content[field] = form.get(field)

    if (tipoAtividade == 'estudo'):
        atividade_list = atividade_list.filter(materia__startswith=content["materia"]or"")
    elif (tipoAtividade == 'conhecer'):
        atividade_list = atividade_list.filter(interesses__startswith=content["interesses"]or"")
    elif (tipoAtividade == 'extracurricular'):
        atividade_list = atividade_list.filter(atividade__startswith=content["atividade"]or"")
    elif (tipoAtividade == 'liga'):
        atividade_list = atividade_list.filter(nomeLiga__startswith=content["nomeLiga"]or"")

    if (tipoAtividade == 'carona'):
        atividade_list = atividade_list.filter(localSaida__startswith=content["localSaida"]or"")
        atividade_list = atividade_list.filter(localChegada__startswith=content["localChegada"]or"")
    else:
        atividade_list = atividade_list.filter(local__startswith=content["local"]or"")

    atividade_list = atividade_list.filter(vagas__gt=int(content["vagas"]or 0))
    atividade_list = atividade_list.filter(adicionais__startswith=content["adicionais"]or"")

    return atividade_list

def listaAtividades(request):
    tipoAtividade = pegarTipoAtividade(request)
    atividades = Atividade.objects.filter(tipo=tipoAtividade).values() #to update with filters

    if (tipoAtividade == 'estudo'):
        filtro_form = estudosFilter()
    elif (tipoAtividade == 'carona'):
        filtro_form = caronaFilter()
    elif (tipoAtividade == 'extracurricular'):
        filtro_form = extraFilter()
    elif (tipoAtividade == 'conhecer'):
        filtro_form = estudosFilter()
    elif (tipoAtividade == 'liga'):
        filtro_form = estudosFilter()

    if request.method == "GET":
        for atividade in atividades:
            atividade['nomeUser'] = "User not found"
            if 'criador_id' in atividade and atividade['criador_id']!="NULL":
                user = User.objects.get(pk=atividade['criador_id'])
                name = user.username
                if name:
                    atividade['nomeUser'] = name
                    continue

    elif request.method == "POST":
       #Filtrar atividade
        atividades = filtrar_atividade(request,atividades,tipoAtividade)

    context = pegarContext(tipoAtividade)

    context['lista'] = atividades
    context['fitro_form'] = filtro_form

    return render(request, 'psiu/lista_atividades.html',context)

def apagar_atividade(request, id):
    tipoAtividade = pegarTipoAtividade(request)
    atividade = Atividade.objects.get(pk = id)

    if (request.user == atividade.criador):
        atividade.delete()

    if (tipoAtividade == 'estudo'):
            return redirect(reverse('psiu:grupo_estudos'))
    if (tipoAtividade == 'carona'):
        return redirect(reverse('psiu:carona'))
    if (tipoAtividade == 'extracurricular'):
        return redirect(reverse('psiu:extracurriculares'))
    if (tipoAtividade == 'conhecer'):
        return redirect(reverse('psiu:conhecer_pessoas'))
    if (tipoAtividade == 'liga'):
        return redirect(reverse('psiu:liga'))

    return redirect(reverse('home'))


def participar_atividade(request, id):
    atividade = Atividade.objects.get(pk = id)

    try:
        participante = ParticipacaoAtividade.objects.get(id_participante=request.user,id_grupo=atividade)
    except:
        participante = None
        participante = ParticipacaoAtividade(id_participante=request.user, id_grupo=atividade, rol='Participante')
        participante.save()

    tipoAtividade = pegarTipoAtividade(request)
    context = pegarContext(tipoAtividade)
    link = context['link_info']

    return redirect('../../psiu/%s/%s'%(link,id))

def sair_atividade(request, id):
    atividade = Atividade.objects.get(pk = id)
    if (request.user != atividade.criador):
        try:
            participante = ParticipacaoAtividade.objects.get(id_participante=request.user,id_grupo=atividade)
            participante.delete()
        except:
            participante = None

    tipoAtividade = pegarTipoAtividade(request)
    context = pegarContext(tipoAtividade)
    link = context['link_info']

    return redirect('../../psiu/%s/%s'%(link,id))


def pegarTipoAtividade(request):
    tipo = request.get_full_path()
    tipo = tipo.split('/')
    tipo = tipo[2]
    if ("estudo" in tipo):
        return 'estudo'
    if ("carona" in tipo):
        return 'carona'
    if ("extracurricular" in tipo):
        return 'extracurricular'
    if ("conhecer" in tipo):
        return 'conhecer'
    if ("liga" in tipo):
        return 'liga'

    return None

def pegarContext(tipoAtividade):
    context = {}

    context['tipo'] = tipoAtividade

    if (tipoAtividade == 'estudo'):
        context['principal'] = 'grupo_estudos'
        context['link_info'] = 'info_estudos'
        context['criar'] = 'criar_estudos'
        context['maiusculo']='Grupo de estudos'
        context['minusculo']='grupo de estudos'
        context['plural']='grupos de estudos'
        context['apagar']='apagar_estudos'
        context['participar']='participar_estudos'
        context['sair']='sair_estudos'
    elif (tipoAtividade == 'carona'):
        context['principal'] = 'carona'
        context['link_info'] = 'info_carona'
        context['criar'] = 'criar_carona'
        context['maiusculo']='Carona'
        context['minusculo']='carona'
        context['plural']='caronas'
        context['apagar']='apagar_carona'
        context['participar']='participar_carona'
        context['sair']='sair_carona'
    elif (tipoAtividade == 'extracurricular'):
        context['principal'] = 'extracurriculares'
        context['link_info'] = 'info_extracurricular'
        context['criar'] = 'criar_extracurricular'
        context['maiusculo']='Atividade extracurricular'
        context['minusculo']='atividade extracurricular'
        context['plural']= 'extracurriculares'
        context['apagar']='apagar_extracurricular'
        context['participar']='participar_extracurricular'
        context['sair']='sair_extracurricular'
    elif (tipoAtividade == 'conhecer'):
        context['principal'] = 'conhecer_pessoas'
        context['link_info'] = 'info_conhecer'
        context['criar'] = 'criar_conhecer'
        context['maiusculo']='Conhecer Pessoas'
        context['minusculo']='atividade'
        context['plural']= 'atividades'
        context['apagar']='apagar_conhecer'
        context['participar']='participar_conhecer'
        context['sair']='sair_conhecer'
    elif (tipoAtividade == 'liga'):
        context['principal'] = 'ligas'
        context['link_info'] = 'info_liga'
        context['criar'] = 'criar_liga'
        context['maiusculo']='Liga'
        context['minusculo']='liga'
        context['plural']= 'ligas'
        context['apagar']='apagar_liga'
        context['participar']='participar_liga'
        context['sair']='sair_liga'

    return context