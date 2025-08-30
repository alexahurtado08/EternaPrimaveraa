#Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido, Pago
from .forms import PagoForm
from carrito.models import Carrito  # si tienes un modelo de carrito
from pedidos.models import Pedido, PedidoItem
from django.utils import timezone
from django.contrib import messages
from usuarios.decorators import admin_required

@login_required
def hacer_pedido(request):
    carrito = Carrito.objects.get(usuario=request.user)
    items = carrito.items.all()
    
    if not items:
        return redirect("carrito:ver_carrito")
    
    pedido = Pedido.objects.create(
        usuario=request.user,
        fecha=timezone.now(),
        total=sum(item.producto.precio * item.cantidad for item in items),
        estado="Pendiente"
    )

    for item in items:
        PedidoItem.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )
    
    items.delete()
    return redirect("pedidos:detalle_pedido", pedido_id=pedido.id)


@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "pedidos/detalle_pedido.html", {"pedido": pedido})


@login_required
def pagar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.pedido = pedido
            pago.total = pedido.total
            pago.save()
            pedido.estado = 'Pagado'
            pedido.save()
            return redirect('pedidos:ver_pago', pago_id=pago.id)
    else:
        form = PagoForm()
    
    return render(request, 'pedidos/pagar_pedido.html', {'form': form, 'pedido': pedido})


@login_required
def ver_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, pedido__usuario=request.user)
    return render(request, 'pedidos/ver_pago.html', {'pago': pago})


#vistas admin----------------------------------------------------------------------------------------------------

def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    try:
        pedido.cambiar_estado(nuevo_estado)
        messages.success(request, f"El estado del pedido {pedido.id} cambió a {nuevo_estado}.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('ver_pedido', pedido_id=pedido.id)


def cambiar_estado_pago(request, pago_id, nuevo_estado):
    pago = get_object_or_404(Pago, id=pago_id)
    try:
        pago.cambiar_estado(nuevo_estado)
        messages.success(request, f"El estado del pago {pago.id} cambió a {nuevo_estado}.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('detalle_pedido', pedido_id=pago.pedido.id)

def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})