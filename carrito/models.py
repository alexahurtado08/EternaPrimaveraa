from django.db import models
from django.contrib.auth.models import User
from producto.models import Producto

class Carrito(models.Model):
    # Si hay usuario logueado, un carrito por usuario
    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="carrito",
        null=True, blank=True
    )
    # Si NO hay usuario, usamos la sesión
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True, db_index=True)
    creado = models.DateTimeField(auto_now_add=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def __str__(self):
        if self.usuario:
            return f"Carrito de {self.usuario.username}"
        return f"Carrito de sesión {self.session_key or 'sin-sesion'}"


class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
