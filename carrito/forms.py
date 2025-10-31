# Realizado por Alexandra Hurtado
from django import forms
from django.utils.translation import gettext_lazy as _

# Formulario para actualizar cantidad en el carrito
class CantidadItemForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        label=_('Cantidad'),
        help_text=_('Ingresa la cantidad deseada (mínimo 1).')
    )
