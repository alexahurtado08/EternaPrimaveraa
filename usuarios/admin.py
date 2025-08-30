#Realizado por Mariana Valderrama
from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'correo', 'telefono')
    search_fields = ('nombre', 'correo')
