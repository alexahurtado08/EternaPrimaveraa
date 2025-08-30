#Realizado por Alexandra Hurtado
from django.db import models

# Modelo que representa un producto disponible en el e-commerce.
class Producto(models.Model):
    
    nombre = models.CharField(max_length=100)  # Nombre del producto
    descripcion = models.TextField()  # Descripción detallada
    cantidad = models.PositiveIntegerField(help_text="Cantidad en gramos")
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio con decimales
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Imagen opcional

    def __str__(self):
        return self.nombre
