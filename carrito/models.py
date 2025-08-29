from django.db import models
from producto.models import Producto
from usuarios.models import Usuario

# Cada usuario tiene un carrito
class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.nombre}"

    # Total del carrito
    def total_carrito(self):
        total = sum(item.subtotal() for item in self.items.all())
        return total

# Cada producto en el carrito
class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"

    # Subtotal por item
    def subtotal(self):
        return self.producto.precio * self.cantidad
