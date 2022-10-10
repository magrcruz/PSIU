from psiu.views_common import *

def filtrar_extra(request, extra_list):
    '''
    carona = Extra()

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
    '''
    return extra_list

def extracurriculares(request):
    extra_list = Extra.objects.all().values()
    print(extra_list)
    fitro_form = None#caronaFilter()
    if request.method == "GET":
        for extra in extra_list:
            extra['nomeUser'] = "User not found"
            if 'criador_id' in extra and extra['criador_id']!="NULL":
                user = User.objects.get(pk=extra['criador_id'])
                name = user.first_name
                if name:
                    extra['nomeUser'] = name

    elif request.method == "POST":
        extra_list = filtrar_extra(request,extra_list)

    return render(request, 'psiu/extracurriculares.html',{'title':'Atividades Extracurriculares', 'extracurriculares':extra_list,'fitro_form':fitro_form})

def criar_extracurricular(request):
    print(request.user)
    if request.method == "GET":
        extra_temp = None
        return render(request, 'psiu/criar_extracurricular.html', {'extra_temp':extra_temp})

    elif request.method == "POST":
        extra = Extra()

        # there is a better way to do this with forms.py
        form = request.POST.dict()
        fields = extra.get_readonly_fields(request)
        content = {} 
        for field in fields:
            if field in form:
                content[field] = form.get(field)
        content['criador_id'] = 1
        content['dataHora'] = datetime.strptime(content['dataHora'], '%Y-%m-%dT%H:%M')

        extra = Extra(**content)
        extra.save()

        return redirect(reverse('psiu:extracurriculares'))

def view_extra(request, id):
    extra = Extra.objects.get(pk = id)
    criador = getTestPerfil()
    try:
        criador = Perfil.objects.get(pk = extra.criador)
    except:
        print("Criador not found")
    return render(request, 'psiu/info_carona.html',{'extra':extra,'contato':criador})