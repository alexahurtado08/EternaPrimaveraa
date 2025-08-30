#Realizado por Alexandra Hurtado
from django.contrib import admin
from .models import Carrito, ItemCarrito

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado_en', 'total_carrito')

@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'carrito', 'cantidad', 'subtotal')
