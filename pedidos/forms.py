from django import forms
from .models import Pedido, Pago

# Formulario para crear/editar pedidos
class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado', 'total']   # producto lo manejamos en la vista



# Formulario para crear/editar pagos
class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['pedido', 'metodo_pago', 'estado']
