from .views_common import *

def filtrar_extra(request, extra_list):
    
    extra = Extra()

    # there is a better way to do this with forms.py
    form = extraFilter(request.POST)
    if form.is_valid():
        fields = extra.get_readonly_fields(request)
        filtro = {}
        
        for field in fields:
            if field in form.cleaned_data:
                filtro[field] = form.cleaned_data[field]

    extra_list = extra_list.filter(atividade__startswith=form.cleaned_data["atividade"]or"")
    extra_list = extra_list.filter(localSaida__startswith=form.cleaned_data["localSaida"]or"")
    extra_list = extra_list.filter(localChegada__startswith=form.cleaned_data["localChegada"]or"")
    extra_list = extra_list.filter(vagas__startswith=form.cleaned_data["vagas"]or"")
    extra_list = extra_list.filter(adicionais__startswith=form.cleaned_data["adicionais"]or"")


    return extra_list

def extracurriculares(request):
    extra_list = Extra.objects.all().values()
    fitro_form = extraFilter()
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

def info_extracurricular(request, id):
    extra = Extra.objects.get(pk = id)
    criador = getTestPerfil()
    try:
        criador = Perfil.objects.get(pk = extra.criador)
    except:
        print("Criador not found")
    return render(request, 'psiu/info_extracurricular.html',{'extra':extra,'contato':criador})