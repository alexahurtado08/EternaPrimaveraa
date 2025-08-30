#Realizado por Alexandra Hurtado
from django.contrib import admin
from .models import Pedido, PedidoItem, Pago



class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0
    readonly_fields = ("subtotal",)


class PagoInline(admin.StackedInline):
    model = Pago
    extra = 0
    readonly_fields = ("fecha",)



@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "estado", "fecha", "total")
    list_filter = ("estado", "fecha")
    search_fields = ("usuario__username", "id")
    inlines = [PedidoItemInline, PagoInline]



@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "producto", "cantidad", "precio", "subtotal")
    list_filter = ("pedido",)
    search_fields = ("producto", "pedido__id")



@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "metodo", "estado", "fecha", "total")
    list_filter = ("estado", "metodo", "fecha")
    search_fields = ("pedido__id", "id")
