# Realizado por Alexandra Hurtado
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Pedido, PedidoItem, Pago


class PedidoItemInline(admin.TabularInline):
    """
    Permite visualizar los ítems del pedido dentro del admin de Pedido.
    """
    model = PedidoItem
    extra = 0
    readonly_fields = ("subtotal",)
    verbose_name = _("Ítem de pedido")
    verbose_name_plural = _("Ítems del pedido")


class PagoInline(admin.StackedInline):
    """
    Permite visualizar el pago asociado dentro del admin de Pedido.
    """
    model = Pago
    extra = 0
    readonly_fields = ("fecha",)
    verbose_name = _("Pago")
    verbose_name_plural = _("Pagos")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para el modelo Pedido.
    """
    list_display = ("id", "usuario", "estado", "fecha", "total")
    list_filter = ("estado", "fecha")
    search_fields = ("usuario__correo", "id")
    inlines = [PedidoItemInline, PagoInline]

    verbose_name = _("Pedido")
    verbose_name_plural = _("Pedidos")


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para los ítems de los pedidos.
    """
    list_display = ("id", "pedido", "producto", "cantidad", "precio", "subtotal")
    list_filter = ("pedido",)
    search_fields = ("producto", "pedido__id")

    verbose_name = _("Ítem de pedido")
    verbose_name_plural = _("Ítems de pedidos")


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    """
    Configuración del panel de administración para los pagos.
    """
    list_display = ("id", "pedido", "metodo", "estado", "fecha", "total")
    list_filter = ("estado", "metodo", "fecha")
    search_fields = ("pedido__id", "id")

    verbose_name = _("Pago")
    verbose_name_plural = _("Pagos")
