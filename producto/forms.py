# Realizado por Alexandra Hurtado
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Producto

# Formulario para crear y editar productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'precio', 'imagen']
        labels = {
            'nombre': _('Nombre'),
            'descripcion': _('Descripción'),
            'cantidad': _('Cantidad'),
            'precio': _('Precio'),
            'imagen': _('Imagen'),
        }
        help_texts = {
            'cantidad': _('Cantidad en gramos.'),
            'precio': _('Introduce el precio con dos decimales.'),
            'imagen': _('Opcional: selecciona una imagen del producto.'),
        }
