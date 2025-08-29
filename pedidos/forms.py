from django import forms
from .models import Pago

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['metodo']
        widgets = {
            'metodo': forms.Select(attrs={'class': 'form-select'}),
        }
