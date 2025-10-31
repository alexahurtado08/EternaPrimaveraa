# Realizado por Alexandra Hurtado
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Producto.
    Permite gestionar los productos del sistema.
    """
    list_display = ('nombre', 'cantidad', 'precio')  # Columnas visibles en la lista
    search_fields = ('nombre',)  # Campo de búsqueda
    list_filter = ('precio',)  # Filtros laterales

    # Nombres traducibles en el panel de administración
    verbose_name = _("Producto")
    verbose_name_plural = _("Productos")
