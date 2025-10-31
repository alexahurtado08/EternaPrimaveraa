# Realizado por Alexandra Hurtado
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Carrito, ItemCarrito


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Carrito.
    """
    list_display = ('usuario', 'creado_en', 'total_carrito')

    # Títulos traducibles
    list_display_links = ('usuario',)
    list_filter = ('creado_en',)
    search_fields = ('usuario__nombre',)

    # Texto traducible para el panel
    verbose_name = _("Carrito")
    verbose_name_plural = _("Carritos")


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo ItemCarrito.
    """
    list_display = ('producto', 'carrito', 'cantidad', 'subtotal')

    list_display_links = ('producto',)
    list_filter = ('carrito',)
    search_fields = ('producto__nombre',)

    verbose_name = _("Item del carrito")
    verbose_name_plural = _("Items del carrito")
