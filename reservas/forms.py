#Realizado por Mariana Valderrama
from django import forms
from .models import Reserva
from datetime import timedelta

#Realizado por Mariana Valderrama
from django import forms
from .models import Reserva
from datetime import timedelta

class ReservaForm(forms.ModelForm):
    """
    Formulario para crear o actualizar reservas.
    Se encarga de la validación de entradas.
    """
    
    PLAN_DURACIONES = {
        'basico': 0,   # 1 día
        'premium': 1,  # 2 días(1 noche)
        'vip': 2,      # 3 días(2 noches)
    }

    class Meta:
        model = Reserva
        fields = ['tipo_plan','fecha_llegada', 'fecha_salida', 'numero_personas']
        widgets = {
            'tipo_plan': forms.Select(attrs={'class': 'form-control'}),
            'fecha_llegada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean(self):
        cleaned_data = super().clean()
        plan = cleaned_data.get('tipo_plan')
        llegada = cleaned_data.get('fecha_llegada')
        salida = cleaned_data.get('fecha_salida')

        if llegada and salida and plan:
            # Duración esperada según plan
            dias_esperados = self.PLAN_DURACIONES.get(plan)
            salida_correcta = llegada + timedelta(days=dias_esperados)

            if salida != salida_correcta:
                self.add_error(
                    'fecha_salida',
                    f"Para el plan {plan}, la salida debe ser {salida_correcta}."
                )

        return cleaned_data


