from psiu.views_common import *
from psiuChat.models import *

def filtrar_carona(request, carona_list):
    carona = Carona()

    # there is a better way to do this with forms.py
    form = caronaFilter(request.POST)
    if form.is_valid():
        fields = carona.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    #carona_list = carona_list.filter(criador__startswith=form.cleaned_data["criador"])
    carona_list = carona_list.filter(localSaida__startswith=form.cleaned_data["localSaida"]or"")
    carona_list = carona_list.filter(localChegada__startswith=form.cleaned_data["localChegada"]or"")
    #carona_list = carona_list.filter(dataHora__startswith=str(datetime.strptime(form.cleaned_data['dataHora'], '%Y-%m-%dT%H:%M'))or"")
    carona_list = carona_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    carona_list = carona_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")

    return carona_list

def carona(request):
    carona_list = Carona.objects.all().values() #to update with filters

    fitro_form = caronaFilter()
    if request.method == "GET":
        for carona in carona_list:
            if 'criador_id' in carona and carona['criador_id']!="NULL":
                user = User.objects.get(pk=carona['criador_id'])
                name = user.first_name
                if name:
                    carona['nomeUser'] = name
                    continue
            carona['nomeUser'] = "User not found"

    elif request.method == "POST":
        carona_list = filtrar_carona(request,carona_list)

    return render(request, 'psiu/carona.html',{'title':'Carona', 'carona_list':carona_list,'fitro_form':fitro_form})

def criar_carona(request):
    print(request)
    if request.method == "GET":
        carona_temp = None
        return render(request, 'psiu/criar_carona.html', {'carona_temp':carona_temp})

    elif request.method == "POST":
        carona = Carona()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = carona.get_readonly_fields(request)
        content = {} 
        for field in fields:
            if field in form:
                content[field] = form.get(field)

        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')
        content['criador_id'] = request.user.id

        carona = Carona(**content)
        carona.save()

        return redirect(reverse('psiu:carona'))

def view_carona(request, id):
    carona = Carona.objects.get(pk = id)
    criador = getTestPerfil()
    try:
        criador = Perfil.objects.get(pk = carona.criador)
    except:
        print("Criador not found")
    return render(request, 'psiu/info_carona.html',{'carona':carona,'contato':criador})