# Realizado por Alexandra Hurtado
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings   # Para usar el modelo de usuario configurado en AUTH_USER_MODEL


# --------------------- MODELO PEDIDO ---------------------
class Pedido(models.Model):
    # Posibles estados de un pedido
    ESTADOS = [
        ('pendiente', _('Pendiente')),
        ('procesado', _('Procesado')),
        ('entregado', _('Entregado')),
    ]

    # Relación con el usuario (un usuario puede tener muchos pedidos)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,   # Si se borra el usuario, se borran sus pedidos
        related_name="pedidos",
        verbose_name=_("usuario")
    )
    # Estado actual del pedido
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name=_("estado"))
    # Fecha de creación del pedido
    fecha = models.DateTimeField(default=timezone.now, verbose_name=_("fecha"))
    # Total del pedido
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_("total"))

    class Meta:
        verbose_name = _("pedido")
        verbose_name_plural = _("pedidos")

    # Método para cambiar el estado del pedido
    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError(_("Estado inválido para el pedido"))

    def __str__(self):
        # Representación en texto
        return _("Pedido %(id)s - %(estado)s") % {'id': self.id, 'estado': self.estado}


# --------------------- MODELO PEDIDO ITEM ---------------------
class PedidoItem(models.Model):
    # Relación con el pedido (un pedido puede tener muchos items)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="items", verbose_name=_("pedido"))
    # Producto (aquí como texto, pero lo ideal sería un ForeignKey a Producto)
    producto = models.CharField(max_length=100, verbose_name=_("producto"))
    # Cantidad de unidades del producto
    cantidad = models.PositiveIntegerField(default=1, verbose_name=_("cantidad"))
    # Precio unitario del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("precio"))

    class Meta:
        verbose_name = _("ítem del pedido")
        verbose_name_plural = _("ítems del pedido")

    # Subtotal = precio x cantidad
    def subtotal(self):
        return self.cantidad * self.precio

    def __str__(self):
        # Representación en texto: "<producto> x <cantidad>"
        return _("%(producto)s x %(cantidad)d") % {'producto': self.producto, 'cantidad': self.cantidad}


# --------------------- MODELO PAGO ---------------------
class Pago(models.Model):
    # Métodos de pago disponibles
    METODO_CHOICES = [
        ('tarjeta', _('Tarjeta')),
        ('paypal', _('Paypal')),
        ('efectivo', _('Efectivo')),
    ]
    # Estados posibles del pago
    ESTADOS = [
        ('pendiente', _('Pendiente')),
        ('pagado', _('Pagado')),
    ]

    # Relación uno a uno: cada pedido tiene un único pago
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name="pago", verbose_name=_("pedido"))
    metodo = models.CharField(max_length=20, choices=METODO_CHOICES, verbose_name=_("método de pago"))  # Método de pago elegido
    fecha = models.DateTimeField(default=timezone.now, verbose_name=_("fecha de pago"))                # Fecha del pago
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("total pagado"))       # Monto pagado
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente', verbose_name=_("estado del pago"))  # Estado del pago

    class Meta:
        verbose_name = _("pago")
        verbose_name_plural = _("pagos")

    # Método para cambiar el estado del pago
    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in dict(self.ESTADOS):
            self.estado = nuevo_estado
            self.save()
        else:
            raise ValueError(_("Estado inválido para el pago"))

    def __str__(self):
        # Representación en texto
        return _("Pago %(id)s - %(estado)s") % {'id': self.id, 'estado': self.estado}
