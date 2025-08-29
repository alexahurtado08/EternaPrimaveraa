from django import forms
from .models import ItemCarrito

# Formulario para agregar producto al carrito
class ItemCarritoForm(forms.ModelForm):
    class Meta:
        model = ItemCarrito
        fields = ['cantidad']
