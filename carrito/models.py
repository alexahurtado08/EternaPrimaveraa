# Realizado por Alexandra Hurtado
from django.db import models
from producto.models import Producto
from usuarios.models import Usuario

# Modelo Carrito: cada usuario tiene un carrito
class Carrito(models.Model):
    # Relación uno a uno: un usuario solo puede tener un carrito
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    # Fecha y hora en que se creó el carrito
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Representación en texto: "Carrito de <nombre del usuario>"
        return f"Carrito de {self.usuario.nombre}"

    # Método para calcular el total del carrito
    def total_carrito(self):
        # Suma los subtotales de todos los items del carrito
        total = sum(item.subtotal() for item in self.items.all())
        return total

# Modelo ItemCarrito: representa un producto dentro del carrito
class ItemCarrito(models.Model):
    # Relación con el carrito (un carrito puede tener varios items)
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    # Relación con el producto (cada item corresponde a un producto)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    # Cantidad de unidades del producto en el carrito
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        # Representación en texto: "<nombre del producto> x <cantidad>"
        return f"{self.producto.nombre} x {self.cantidad}"

    # Método para calcular el subtotal de este item
    def subtotal(self):
        # Precio del producto multiplicado por la cantidad
        return self.producto.precio * self.cantidad
