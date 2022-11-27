from .views_common import *
from psiuChat.models import *

def filtrar_conhecer(request, conhecer_list):
    conhecer = Conhecer()
    form = request.POST.dict()
    fields = conhecer.get_readonly_fields(request)
    content = {} 
    for field in fields:
        if field in form:
            content[field] = form.get(field)
    
    conhecer_list = conhecer_list.filter(interesses__startswith=content["interesses"]or"")
    conhecer_list = conhecer_list.filter(local__startswith=content["local"]or"")
    conhecer_list = conhecer_list.filter(vagas__gt=int(content["vagas"]or 0))
    conhecer_list = conhecer_list.filter(adicionais__startswith=content["adicionais"]or"")

    return conhecer_list

def conhecer_pessoas(request):
    conhecer_list = Conhecer.objects.all().values() #to update with filters

    #fitro_form = conhecerFilter()
    if request.method == "GET":
        for conhecer in conhecer_list:
            if 'criador_id' in conhecer and conhecer['criador_id']!="NULL":
                user = User.objects.get(pk=conhecer['criador_id'])
                name = user.first_name
                if name:
                    conhecer['nomeUser'] = name
                    continue
            conhecer['nomeUser'] = "User not found"

    elif request.method == "POST":
        conhecer_list = filtrar_conhecer(request,conhecer_list)

    return render(request, 'psiu/lista_conhecer_pessoas.html',{'title':'Conhecer', 'conhecer_list':conhecer_list,'fitro_form':None})

def criar_pessoas(request):
    if request.method == "GET":
        conhecer_temp = None
        return render(request, 'psiu/criar_pessoas.html', {'conhecer_temp':conhecer_temp})

    elif request.method == "POST":
        conhecer = Conhecer()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = conhecer.get_readonly_fields(request)
        content = {} 
        for field in fields:
            if field in form:
                content[field] = form.get(field)

        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')
        content['criador_id'] = request.user.id

        conhecer = Conhecer(**content)
        conhecer.save()

        return redirect(reverse('psiu:conhecer_pessoas'))

def view_conhecer(request, id):
    conhecer = Conhecer.objects.get(pk = id)
    return render(request, 'psiu/info_conhecer.html',{'conhecer':conhecer,'contato':getContato(conhecer.criador)
})

def info_conhecer(request, id):
    formnewParticipante = newParticipante()

    if request.method == "POST":
        form = request.POST.dict()
        content = {
            'id_participante':User.objects.get(pk = form.get('id_participante')),
            'id_grupo':Conhecer.objects.get(pk = id),
            'rol':form.get('rol')
        }
        conhecer = ParticipacaoConhecer(**content)
        #carona.add_to_class('dataHora', content['dataHora'])
        conhecer.save()

    pessoa = Conhecer.objects.get(pk = id)
    participantes = list(ParticipacaoConhecer.objects.all().values().filter(id_grupo=id).values())

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



    if (request.user == pessoa.criador):
        isCriador = True
    else:
        isCriador = False

    criador = getTestPerfil()
    return render(request, 'psiu/info_conhecer.html',{'pessoa':pessoa,'contato':criador, 
    'participantes':participantes,'form':formnewParticipante,
    'isCriador':isCriador,'isParticipante':isParticipante})

def apagar_conhecer(request):
    return redirect(reverse('psiu:conhecer'))