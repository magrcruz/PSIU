from .views_common import *
from django.http import HttpResponseRedirect

# GRUPO DE ESTUDOS
def info_estudos(request, id):
    formnewParticipante = newParticipante()

    if request.method == "POST":
        form = request.POST.dict()
        content = {
            'id_participante':User.objects.get(pk = form.get('id_participante')),
            'id_grupo':Estudos.objects.get(pk = id),
            'rol':form.get('rol')
        }
        estudos = ParticipacaoGrupoEstudos(**content)
        #carona.add_to_class('dataHora', content['dataHora'])
        estudos.save()

    grupo = Estudos.objects.get(pk = id)
    participantes = list(ParticipacaoGrupoEstudos.objects.all().values().filter(id_grupo=id).values())

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



    if (request.user == grupo.criador):
        isCriador = True
    else:
        isCriador = False

    criador = getTestPerfil()
    return render(request, 'psiu/info_estudos.html',{'grupo':grupo,'contato':getContato(grupo.criador), 
    'participantes':participantes,'form':formnewParticipante,
    'isCriador':isCriador,'isParticipante':isParticipante})

def criar_estudos(request):
    if request.method == "GET":
        return render(request, 'psiu/criar_estudos.html', {})

    elif request.method == "POST":
        estudos = Estudos()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = estudos.get_readonly_fields(request)
        content = {}
        for field in fields:
            if field in form:
                content[field] = form.get(field)
        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')

        new_room = Room.objects.create()
        new_room.save()

        content['criador_id'] = request.user.id
        
        estudos = Estudos(**content, sala=new_room)
        estudos.save()

        participante = ParticipacaoGrupoEstudos(id_participante=request.user, id_grupo=estudos, rol="Criador")
        participante.save()

        return redirect(reverse('psiu:grupo_estudos'))

def filtrar_estudos(request, estudos_list):
    estudos = Estudos()

    # there is a better way to do this with forms.py
    form = estudosFilter(request.POST)
    if form.is_valid():
        fields = estudos.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    estudos_list = estudos_list.filter(materia__startswith=form.cleaned_data["materia"]or"")
    estudos_list = estudos_list.filter(local__startswith=form.cleaned_data["local"]or"")
    #estudos_list = estudos_list.filter(dataHora__startswith=str(datetime.strptime(form.cleaned_data['dataHora'], '%Y-%m-%dT%H:%M'))or"")
    estudos_list = estudos_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    estudos_list = estudos_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")

    return estudos_list

def grupo_estudos(request):
    grupo_de_estudos = Estudos.objects.all().values() #to update with filters

    fitro_form = estudosFilter()
    if request.method == "GET":
        for grupo in grupo_de_estudos:
            grupo['nomeUser'] = "User not found"
            if 'criador_id' in grupo and grupo['criador_id']!="NULL":
                user = User.objects.get(pk=grupo['criador_id'])
                name = user.first_name
                if name:
                    grupo['nomeUser'] = name
                    continue

    elif request.method == "POST":
       #Filtrar grupo de estudos
        grupo_de_estudos = filtrar_estudos(request,grupo_de_estudos)

    return render(request, 'psiu/estudos.html',{'title':'Grupo de estudos','grupo_estudos':grupo_de_estudos,'fitro_form':fitro_form})

def apagar_estudos(request, id):
    grupo = Estudos.objects.get(pk = id)
    if (request.user == grupo.criador):
        grupo.delete()

    return redirect(reverse('psiu:grupo_estudos'))

def participar_estudos(request, id):
    grupo = Estudos.objects.get(pk = id)
    try:
        participante = ParticipacaoGrupoEstudos.objects.get(id_participante=request.user,id_grupo=grupo)
    except:
        participante = None
        participante = ParticipacaoGrupoEstudos(id_participante=request.user, id_grupo=grupo, rol='Participante')
        participante.save()
    return redirect('../../psiu/info_estudos/%s'%id)

def sair_estudos(request, id):
    grupo = Estudos.objects.get(pk = id)
    if (request.user != grupo.criador):
        try:
            participante = ParticipacaoGrupoEstudos.objects.get(id_participante=request.user,id_grupo=grupo)
            participante.delete()
        except:
            participante = None

    return redirect('../../psiu/info_estudos/%s'%id)