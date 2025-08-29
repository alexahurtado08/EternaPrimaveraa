from django import forms

# Form para actualizar cantidad en carrito
class CantidadItemForm(forms.Form):
    cantidad = forms.IntegerField(min_value=1, label='Cantidad')
