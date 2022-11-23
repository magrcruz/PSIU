from .views_common import *
from psiuChat.models import *

def filtrar_conhecer(request, conhecer_list):
    conhecer = Conhecer()

    # there is a better way to do this with forms.py
    '''form = conhecerFilter(request.POST)
    if form.is_valid():
        fields = conhecer.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    #conhecer_list = conhecer_list.filter(criador__startswith=form.cleaned_data["criador"])
    conhecer_list = conhecer_list.filter(localSaida__startswith=form.cleaned_data["localSaida"]or"")
    conhecer_list = conhecer_list.filter(localChegada__startswith=form.cleaned_data["localChegada"]or"")
    #conhecer_list = conhecer_list.filter(dataHora__startswith=str(datetime.strptime(form.cleaned_data['dataHora'], '%Y-%m-%dT%H:%M'))or"")
    conhecer_list = conhecer_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    conhecer_list = conhecer_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")
'''
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

    return render(request, 'psiu/conhecer_pessoas.html',{'title':'Conhecer', 'conhecer_list':conhecer_list,'fitro_form':None})

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
    criador = getTestPerfil()
    try:
        criador = Perfil.objects.get(pk = conhecer.criador)
    except:
        print("Criador not found")
    print(conhecer.__dict__)
    return render(request, 'psiu/info_conhecer.html',{'conhecer':conhecer,'contato':criador})

def apagar_conhecer(request):
    return redirect(reverse('psiu:conhecer'))