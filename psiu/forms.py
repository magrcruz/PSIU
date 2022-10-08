from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from .models import Carona, Perfil, Estudos, ParticipacaoGrupoEstudos

# Create your forms here.

class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={"class": "form-control"}))
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username',"class": "form-control"})
        self.fields['first_name'].widget.attrs.update({"class": "form-control"})
        self.fields['last_name'].widget.attrs.update({"class": "form-control"})
        self.fields['password1'].widget.attrs.update({"class": "form-control"})
        self.fields['password2'].widget.attrs.update({"class": "form-control"})


class ModificarPerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('fotoPerfil','bio','twitter','instagram')

    def __init__(self, user, *args, **kwargs):
        #self.user = user
        #user.objects.get(place=p1)
        super().__init__(*args, **kwargs)
        self.fields['bio'].widget.attrs.update({'placeholder': "Bio","class": "form-control"})


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('fotoPerfil',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fotoPerfil'].widget.attrs.update({"class": "form-control"})

class caronaFilter(forms.ModelForm):
    class Meta:
        model = Carona
        fields = ('localSaida', 'localChegada', 'dataHora', 'vagas', 'adicionais')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['criador'].widget.attrs.update({"class": "form-control"})
        self.fields['localSaida'].widget.attrs.update({"class": "form-control"})
        self.fields['localChegada'].widget.attrs.update({"class": "form-control"})
        self.fields['dataHora'].widget.attrs.update({"class": "form-control"})
        self.fields['vagas'].widget.attrs.update({"class": "form-control"})
        self.fields['adicionais'].widget.attrs.update({"class": "form-control"})

class estudosFilter(forms.ModelForm):
    class Meta:
        model = Estudos
        fields = ('materia', 'local', 'dataHora', 'vagas', 'adicionais')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['criador'].widget.attrs.update({"class": "form-control"})
        self.fields['materia'].widget.attrs.update({"class": "form-control"})
        self.fields['local'].widget.attrs.update({"class": "form-control"})
        self.fields['dataHora'].widget.attrs.update({"class": "form-control"})
        self.fields['vagas'].widget.attrs.update({"class": "form-control"})
        self.fields['adicionais'].widget.attrs.update({"class": "form-control"})

class newParticipante(forms.ModelForm):
    class Meta:
        model = ParticipacaoGrupoEstudos
        fields = ('id_participante', 'rol')
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_participante'].widget.attrs.update({"class": "form-control"})
        self.fields['rol'].widget.attrs.update({"class": "form-control"})
