# Realizado por Mariana Valderrama
from django.db import models
from django.utils.translation import gettext_lazy as _

# Modelo que representa una reserva realizada por un cliente
class Reserva(models.Model):
    """
    Modelo para manejar reservas de clientes.
    """

    # Identificador único de la reserva (clave primaria automática)
    id = models.AutoField(primary_key=True, verbose_name=_("ID de la reserva"))

    # Fecha de llegada de la reserva
    fecha_llegada = models.DateField(verbose_name=_("fecha de llegada"))

    # Fecha de salida de la reserva
    fecha_salida = models.DateField(verbose_name=_("fecha de salida"))

    # Número de personas que incluye la reserva
    numero_personas = models.PositiveIntegerField(
        verbose_name=_("número de personas"),
        help_text=_("Cantidad total de personas incluidas en la reserva")
    )

    # Opciones disponibles para el tipo de plan
    PLAN_CHOICES = [
        ('basico', _("Básico")),
        ('premium', _("Premium")),
        ('vip', _("VIP")),
    ]

    # Campo que almacena el plan seleccionado (básico, premium o VIP)
    tipo_plan = models.CharField(
        max_length=20,
        choices=PLAN_CHOICES,
        verbose_name=_("tipo de plan"),
        help_text=_("Seleccione el tipo de plan para la reserva")
    )

    class Meta:
        verbose_name = _("reserva")
        verbose_name_plural = _("reservas")

    def __str__(self):
        # Representación legible de la reserva → muestra el rango de fechas
        return f"{_('Reserva')} {self.id} - {self.fecha_llegada} {_('a')} {self.fecha_salida}"
