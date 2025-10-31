# Realizado por Mariana Valderrama
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Reserva
from datetime import timedelta

# Formulario basado en el modelo Reserva
class ReservaForm(forms.ModelForm):
    """
    Formulario para crear o actualizar reservas.
    Se encarga de la validación de entradas.
    """

    # Duraciones predeterminadas según el tipo de plan
    PLAN_DURACIONES = {
        'basico': 0,   # Plan básico → 1 día (llega y sale el mismo día)
        'premium': 1,  # Plan premium → 2 días (1 noche)
        'vip': 2,      # Plan VIP → 3 días (2 noches)
    }

    class Meta:
        model = Reserva
        # Campos del modelo que se mostrarán en el formulario
        fields = ['tipo_plan', 'fecha_llegada', 'fecha_salida', 'numero_personas']
        
        # Etiquetas traducibles
        labels = {
            'tipo_plan': _('Tipo de plan'),
            'fecha_llegada': _('Fecha de llegada'),
            'fecha_salida': _('Fecha de salida'),
            'numero_personas': _('Número de personas'),
        }

        # Textos de ayuda traducibles
        help_texts = {
            'tipo_plan': _('Selecciona el plan que deseas reservar.'),
            'fecha_llegada': _('Selecciona la fecha en que llegarás al parque.'),
            'fecha_salida': _('La fecha de salida se ajustará automáticamente según el plan.'),
            'numero_personas': _('Número total de visitantes incluidos en la reserva.'),
        }

        # Widgets para dar estilo a los inputs en el formulario
        widgets = {
            'tipo_plan': forms.Select(attrs={'class': 'form-control'}),
            'fecha_llegada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'numero_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def clean(self):
        """
        Validación personalizada:
        - Se asegura de que la fecha de salida coincida con la duración esperada del plan elegido.
        """
        cleaned_data = super().clean()
        plan = cleaned_data.get('tipo_plan')
        llegada = cleaned_data.get('fecha_llegada')
        salida = cleaned_data.get('fecha_salida')

        # Validamos solo si los campos están completos
        if llegada and salida and plan:
            # Duración que debería tener el plan
            dias_esperados = self.PLAN_DURACIONES.get(plan)
            salida_correcta = llegada + timedelta(days=dias_esperados)

            # Si la fecha de salida no coincide con la esperada → error
            if salida != salida_correcta:
                self.add_error(
                    'fecha_salida',
                    _(f"⚠️ Para el plan {plan}, la fecha de salida debe ser {salida_correcta}.")
                )

        return cleaned_data
