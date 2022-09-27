from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from .models import Perfil

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



class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ('fotoPerfil',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fotoPerfil'].widget.attrs.update({"class": "form-control"})
