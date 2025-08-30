#Realizado por Mariana Valderrama
from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    """
    Formulario para crear o actualizar reservas.
    Se encarga de la validación de entradas.
    """
    class Meta:
        model = Reserva
        fields = ['fecha_llegada', 'fecha_salida', 'numero_personas', 'tipo_plan']
        widgets = {
            'fecha_llegada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'tipo_plan': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        llegada = cleaned_data.get('fecha_llegada')
        salida = cleaned_data.get('fecha_salida')
        if llegada and salida and llegada > salida:
            self.add_error('fecha_salida', 'La fecha de salida debe ser posterior a la llegada.')

