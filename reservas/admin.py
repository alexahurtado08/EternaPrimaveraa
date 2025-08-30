#Realizado por Mariana Valderrama
# Register your models here.
from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para el modelo Reserva.
    Muestra los campos importantes y permite búsqueda y filtros.
    """
    list_display = ('id', 'fecha_llegada', 'fecha_salida', 'numero_personas', 'tipo_plan')
    list_filter = ('tipo_plan', 'fecha_llegada', 'fecha_salida')
    search_fields = ('id',)
    ordering = ('-fecha_llegada',)
