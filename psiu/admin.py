from django.contrib import admin

# Register your models here.
from .models import Usuario, Carona, Estudos, Extra, Ligas

admin.site.register(Usuario)
admin.site.register(Carona)
admin.site.register(Estudos)
admin.site.register(Extra)
admin.site.register(Ligas)
