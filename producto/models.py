# Realizado por Alexandra Hurtado
from django.db import models

# Modelo que representa un producto disponible en el e-commerce
class Producto(models.Model):
    
    # Nombre del producto (máximo 100 caracteres)
    nombre = models.CharField(max_length=100)
    # Descripción detallada del producto
    descripcion = models.TextField()
    # Cantidad disponible (ej: en gramos) → solo acepta números positivos
    cantidad = models.PositiveIntegerField(help_text="Cantidad en gramos")
    # Precio del producto (con dos decimales)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    # Imagen opcional del producto (se guarda en la carpeta "productos/")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)

    def __str__(self):
        # Representación en texto → muestra el nombre del producto
        return self.nombre
