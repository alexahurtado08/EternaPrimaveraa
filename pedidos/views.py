#Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido, Pago
from .forms import PagoForm
from carrito.models import Carrito  # si tienes un modelo de carrito
from pedidos.models import Pedido, PedidoItem
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import openpyxl

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
        estado="pendiente"   # 👈 minúscula, para coincidir con choices
    )

    for item in items:
        PedidoItem.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )
    
    # ✅ Crear el pago pendiente automáticamente
    Pago.objects.create(
        pedido=pedido,
        metodo="efectivo",   # 👈 o puedes dejar que elija después
        total=pedido.total,
        estado="pendiente"
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
    pago = pedido.pago  # ✅ ya existe porque lo creamos en hacer_pedido
    
    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)  # ✅ editar el mismo pago
        if form.is_valid():
            pago = form.save(commit=False)
            pago.estado = "pagado"  # ✅ marcar como pagado
            pago.save()
            return redirect('pedidos:ver_pago', pago_id=pago.id)
    else:
        form = PagoForm(instance=pago)
    
    return render(request, 'pedidos/pagar_pedido.html', {'form': form, 'pedido': pedido})


@login_required
def ver_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, pedido__usuario=request.user)
    return render(request, 'pedidos/ver_pago.html', {'pago': pago})


#vistas admin----------------------------------------------------------------------------------------------------

@staff_member_required
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    valores_validos = [estado[0] for estado in Pedido.ESTADOS]  # ['pendiente', 'procesado', 'entregado']

    if nuevo_estado in valores_validos:
        pedido.estado = nuevo_estado
        pedido.save()
        messages.success(
            request,
            f"El estado del pedido {pedido.id} cambió a {pedido.get_estado_display()}."
        )
    else:
        messages.error(request, "Estado no válido.")
    return redirect('pedidos:lista_pedidos')


@staff_member_required
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

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, "pedidos/mis_pedidos.html", {"pedidos": pedidos})



@login_required
def pedido_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    template = get_template("pedidos/pedido_pdf.html")  # 👈 plantilla especial para el PDF
    html = template.render({"pedido": pedido})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="pedido_{pedido.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    
    return response

@staff_member_required
def exportar_pedidos_pagados_excel(request):
    # Solo pedidos cuyo pago está en estado "pagado"
    pedidos = Pedido.objects.filter(pago__estado="pagado")

    # Crear libro y hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pedidos Pagados"

    # Encabezados
    ws.append(["ID", "Cliente", "Dirección", "Fecha", "Total", "Estado Pedido", "Productos"])

    # Filas
    for pedido in pedidos:
        productos_str = ", ".join(
            [f"{item.producto} x{item.cantidad}" for item in pedido.items.all()]
        )
        ws.append([
            pedido.id,
            pedido.usuario.nombre,
            getattr(pedido.usuario, "direccion", "N/A"),
            pedido.fecha.strftime("%Y-%m-%d %H:%M"),
            float(pedido.total),
            pedido.estado,
            productos_str
        ])

    # Respuesta HTTP con el Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="pedidos_pagados.xlsx"'
    wb.save(response)
    return response