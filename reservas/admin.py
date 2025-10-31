# Realizado por Mariana Valderrama
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Reserva


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Reserva.
    Permite gestionar las reservas con filtros, búsqueda y ordenación.
    """
    list_display = ('id', 'fecha_llegada', 'fecha_salida', 'numero_personas', 'tipo_plan')
    list_filter = ('tipo_plan', 'fecha_llegada', 'fecha_salida')
    search_fields = ('id',)
    ordering = ('-fecha_llegada',)

    # Etiquetas traducibles en el panel de administración
    verbose_name = _("Reserva")
    verbose_name_plural = _("Reservas")
