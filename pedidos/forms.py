# Realizado por Alexandra Hurtado
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Pago

# Formulario para registrar o actualizar un pago
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago  # El formulario se basa en el modelo Pago
        fields = ['metodo']  # Solo permitirá elegir el método de pago
        widgets = {
            # Usamos un <select> con clase CSS 'form-select' (ej: Bootstrap)
            'metodo': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {
            'metodo': _('Método de pago'),
        }
        help_texts = {
            'metodo': _('Selecciona el método de pago preferido.'),
        }
