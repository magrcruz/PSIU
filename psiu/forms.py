from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *


# Create your forms here.

class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'placeholder': 'Email','aria-label':'Username','aria-describedby':"addon-wrapping"}))
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Usuario'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar Senha'})