from django.db import models
from django.utils import timezone
from django.conf import settings   # 👈 IMPORTANTE para el usuario

class Pedido(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('entregado', 'Entregado'),
    ]

    usuario = models.ForeignKey(   # 👈 Relacionamos el pedido con el usuario
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="pedidos"
    )
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(default=timezone.now)  # 👈 lo regresamos
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # 👈 lo regresamos

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Estado inválido para el pedido")

    def __str__(self):
        return f"Pedido {self.id} - {self.estado}"


class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    producto = models.CharField(max_length=100)  # o mejor un ForeignKey a tu modelo Producto
    cantidad = models.PositiveIntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        return f"{self.producto} x {self.cantidad}"
    
class Pago(models.Model):
    METODO_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'Paypal'),
        ('efectivo', 'Efectivo'),
    ]
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pago")
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)
    fecha = models.DateTimeField(default=timezone.now)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Estado inválido para el pago")

    def __str__(self):
        return f"Pago {self.id} - {self.estado}"
