from django import forms
from .models import Producto

# Formulario para crear y editar productos.
   
class ProductoForm(forms.ModelForm):
    
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'precio', 'imagen']
