from django.db import models

class Reserva(models.Model):
    """
    Modelo para manejar reservas de clientes.
    """
    id = models.AutoField(primary_key=True)
    fecha_llegada = models.DateField()
    fecha_salida = models.DateField()
    numero_personas = models.PositiveIntegerField()
    
    PLAN_CHOICES = [
        ('basico', 'Básico'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    tipo_plan = models.CharField(max_length=20, choices=PLAN_CHOICES)

    def __str__(self):
        return f"Reserva {self.id} - {self.fecha_llegada} a {self.fecha_salida}"

