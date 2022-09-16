from django.forms import ModelForm
from .models import Usuario

class CriarUsuarioForm(ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"