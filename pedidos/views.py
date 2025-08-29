from django.shortcuts import render, get_object_or_404, redirect
from .models import Pedido, Pago
from .forms import PedidoForm, PagoForm
from producto.models import Producto
from .forms import PedidoForm

# Vista de pedidos


# Crear pedido desde un producto
def crear_pedido_desde_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.producto = producto
            # Si quieres que el total sea automático según precio del producto:
            pedido.total = producto.precio  
            pedido.save()
            return redirect('detalle_pedido', pedido_id=pedido.id)
    else:
        # El total se precarga con el precio del producto
        form = PedidoForm(initial={'total': producto.precio})

    return render(request, 'pedidos/crear_pedido.html', {
        'form': form,
        'producto': producto
    })
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})




# Vistas de pagos


def lista_pagos(request):
    pagos = Pago.objects.all()
    return render(request, 'pedidos/lista_pagos.html', {'pagos': pagos})


def detalle_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    return render(request, 'pedidos/detalle_pago.html', {'pago': pago})


def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pagos')
    else:
        form = PagoForm()
    return render(request, 'pedidos/crear_pago.html', {'form': form})
