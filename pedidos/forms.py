# Realizado por Alexandra Hurtado
from django import forms
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
