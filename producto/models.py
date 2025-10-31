# Realizado por Alexandra Hurtado
from django.db import models
from django.utils.translation import gettext_lazy as _

# Modelo que representa un producto disponible en el e-commerce
class Producto(models.Model):

    # Nombre del producto (máximo 100 caracteres)
    nombre = models.CharField(max_length=100, verbose_name=_("nombre"))
    # Descripción detallada del producto
    descripcion = models.TextField(verbose_name=_("descripción"))
    # Cantidad disponible (ej: en gramos) → solo acepta números positivos
    cantidad = models.PositiveIntegerField(
        help_text=_("Cantidad en gramos"),
        verbose_name=_("cantidad disponible")
    )
    # Precio del producto (con dos decimales)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_("precio")
    )
    # Imagen opcional del producto (se guarda en la carpeta "productos/")
    imagen = models.ImageField(
        upload_to='productos/',
        blank=True,
        null=True,
        verbose_name=_("imagen del producto")
    )

    class Meta:
        verbose_name = _("producto")
        verbose_name_plural = _("productos")

    def __str__(self):
        # Representación en texto → muestra el nombre del producto
        return self.nombre
