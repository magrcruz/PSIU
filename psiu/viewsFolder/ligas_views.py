from .views_common import *
from psiuChat.models import *

def filtrar_ligas(request, ligas_list):
    ligas = Ligas()
    form = request.POST.dict()
    fields = ligas.get_readonly_fields(request)
    content = {} 
    for field in fields:
        if field in form:
            content[field] = form.get(field)
    ligas_list = ligas_list.filter(atividade__startswith=content["atividade"]or"")
    ligas_list = ligas_list.filter(local__startswith=content["local"]or"")
    ligas_list = ligas_list.filter(vagas__gt=int(content["vagas"]or 0))

    return ligas_list

def ligas_nao_oficiais(request):
    ligas_list = Ligas.objects.all().values()
    fitro_form = ligasFilter()
    if request.method == "GET":
        for ligas in ligas_list:
            ligas['nomeUser'] = "User not found"
            if 'criador_id' in ligas and ligas['criador_id']!="NULL":
                user = User.objects.filter(pk=ligas['criador_id'])
                if user: user=user[0]
                else: continue
                name = user.username
                if name:
                    ligas['nomeUser'] = name
                    continue
                ligas['nomeUser'] = "User not found  "

    elif request.method == "POST":
        ligas_list = filtrar_ligas(request,ligas_list)

    return render(request, 'psiu/lista_ligas_nao_oficiais.html',{'title':'Ligas Acadêmicas Não Oficiais', 'ligas_nao_oficiais':ligas_list,'fitro_form':fitro_form})

def criar_ligas(request):
    print(request)
    if request.method == "GET":
        ligas_temp = None
        return render(request, 'psiu/criar_ligas.html', {'ligas_temp':ligas_temp})

    elif request.method == "POST":
        ligas = Ligas()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = ligas.get_readonly_fields(request)
        content = {} 
        for field in fields:
            if field in form:
                content[field] = form.get(field)
        content['criador_id'] = request.user.id
        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')

        sala = Room.objects.create()
        content['sala'] = sala
        ligas = Ligas(**content)
        ligas.save()

        return redirect(reverse('psiu:ligas_nao_oficiais'))
        
def info_ligas_nao_oficiais(request, id):
    ligas = Ligas.objects.get(pk = id)
    return render(request, 'psiu/info_ligas_nao_oficiais.html',{'ligas':ligas,'contato':getContato(ligas.criador)})

def ligas_oficiais(request):
    return render(request, 'psiu/ligas_oficiais.html',{'title':'Ligas Oficiais'})

def ligas_academicas(request):
    return render(request, 'psiu/ligas_academicas.html',{'title':'Ligas Academicas'})