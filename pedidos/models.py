# Realizado por Alexandra Hurtado
from django.db import models
from django.utils import timezone
from django.conf import settings   # Para usar el modelo de usuario configurado en AUTH_USER_MODEL

# --------------------- MODELO PEDIDO ---------------------
class Pedido(models.Model):
    # Posibles estados de un pedido
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado'),
        ('entregado', 'Entregado'),
    ]

    # Relación con el usuario (un usuario puede tener muchos pedidos)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,   # Si se borra el usuario, se borran sus pedidos
        related_name="pedidos"
    )
    # Estado actual del pedido
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    # Fecha de creación del pedido
    fecha = models.DateTimeField(default=timezone.now)
    # Total del pedido
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Método para cambiar el estado del pedido
    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Estado inválido para el pedido")

    def __str__(self):
        # Representación en texto
        return f"Pedido {self.id} - {self.estado}"


# --------------------- MODELO PEDIDO ITEM ---------------------
class PedidoItem(models.Model):
    # Relación con el pedido (un pedido puede tener muchos items)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items")
    # Producto (aquí como texto, pero lo ideal sería un ForeignKey a Producto)
    producto = models.CharField(max_length=100)
    # Cantidad de unidades del producto
    cantidad = models.PositiveIntegerField(default=1)
    # Precio unitario del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    # Subtotal = precio x cantidad
    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        # Representación en texto: "<producto> x <cantidad>"
        return f"{self.producto} x {self.cantidad}"


# --------------------- MODELO PAGO ---------------------
class Pago(models.Model):
    # Métodos de pago disponibles
    METODO_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'Paypal'),
        ('efectivo', 'Efectivo'),
    ]
    # Estados posibles del pago
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    # Relación uno a uno: cada pedido tiene un único pago
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pago")
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES)  # Método de pago elegido
    fecha = models.DateTimeField(default=timezone.now)                # Fecha del pago
    total = models.DecimalField(max_digits=10, decimal_places=2)      # Monto pagado
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')  # Estado del pago

    # Método para cambiar el estado del pago
    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError("Estado inválido para el pago")

    def __str__(self):
        # Representación en texto
        return f"Pago {self.id} - {self.estado}"
