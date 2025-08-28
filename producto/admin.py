from django.contrib import admin
from .models import Producto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'precio')  # columnas visibles
    search_fields = ('nombre',)  # buscador
    list_filter = ('precio',)  # filtros laterales