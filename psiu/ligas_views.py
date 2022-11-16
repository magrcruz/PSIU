from psiu.views_common import *
from psiuChat.models import *

def filtrar_ligas(request, ligas_list):
    
    ligas = Ligas()

    # there is a better way to do this with forms.py
    form = ligasFilter(request.POST)
    
    if form.is_valid():
        fields = ligas.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    ligas_list = ligas_list.filter(atividade__startswith=form.cleaned_data["atividade"]or"")
    ligas_list = ligas_list.filter(local__startswith=form.cleaned_data["local"]or"")
    ligas_list = ligas_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    ligas_list = ligas_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")


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
                name = user.first_name
                if name:
                    ligas['nomeUser'] = name
                    continue
                ligas['nomeUser'] = "User not found  "

    elif request.method == "POST":
        ligas_list = filtrar_ligas(request,ligas_list)

    return render(request, 'psiu/ligas_nao_oficiais.html',{'title':'Ligas Acadêmicas Não Oficiais', 'ligas_nao_oficiais':ligas_list,'fitro_form':fitro_form})

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
    criador = getTestPerfil()
    try:
        criador = Perfil.objects.get(pk = ligas.criador)
    except:
        print("Criador not found")
    return render(request, 'psiu/info_ligas_nao_oficiais.html',{'ligas':ligas,'contato':criador})

def ligas_oficiais(request):
    return render(request, 'psiu/ligas_oficiais.html',{'title':'Ligas Oficiais'})

def ligas_academicas(request):
    return render(request, 'psiu/ligas_academicas.html',{'title':'Ligas Academicas'})