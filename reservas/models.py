# Realizado por Mariana Valderrama
from django.db import models

# Modelo que representa una reserva realizada por un cliente
class Reserva(models.Model):
    """
    Modelo para manejar reservas de clientes.
    """

    # Identificador único de la reserva (clave primaria automática)
    id = models.AutoField(primary_key=True)

    # Fecha de llegada de la reserva
    fecha_llegada = models.DateField()

    # Fecha de salida de la reserva
    fecha_salida = models.DateField()

    # Número de personas que incluye la reserva
    numero_personas = models.PositiveIntegerField()

    # Opciones disponibles para el tipo de plan
    PLAN_CHOICES = [
        ('basico', 'Básico'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]

    # Campo que almacena el plan seleccionado (básico, premium o VIP)
    tipo_plan = models.CharField(max_length=20, choices=PLAN_CHOICES)

    def __str__(self):
        # Representación legible de la reserva → muestra el rango de fechas
        return f"Reserva {self.id} - {self.fecha_llegada} a {self.fecha_salida}"
