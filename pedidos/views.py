# Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Pedido, Pago
from .forms import PagoForm
from carrito.models import Carrito  # Modelo del carrito de compras
from pedidos.models import Pedido, PedidoItem
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import openpyxl

# ---------------- Vistas de usuario ---------------- #

# Crear un pedido a partir de los productos en el carrito
@login_required
def hacer_pedido(request):
    carrito = Carrito.objects.get(usuario=request.user)  # Obtiene el carrito del usuario
    items = carrito.items.all()  # Todos los productos del carrito
    
    if not items:  # Si el carrito está vacío, redirige
        return redirect("carrito:ver_carrito")
    
    # Crear el pedido con los datos del carrito
    pedido = Pedido.objects.create(
        usuario=request.user,
        fecha=timezone.now(),
        total=sum(item.producto.precio * item.cantidad for item in items),
        estado="pendiente"   # Estado inicial del pedido
    )

    # Crear los items del pedido a partir de los items del carrito
    for item in items:
        PedidoItem.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )
    
    # Crear un pago pendiente para el pedido
    Pago.objects.create(
        pedido=pedido,
        metodo="efectivo",   # Puede cambiarse más adelante
        total=pedido.total,
        estado="pendiente"
    )

    # Vaciar el carrito
    items.delete()
    return redirect("pedidos:detalle_pedido", pedido_id=pedido.id)

# Ver el detalle de un pedido
@login_required
def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "pedidos/detalle_pedido.html", {"pedido": pedido})

# Realizar el pago de un pedido
@login_required
def pagar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    pago = pedido.pago  # El pago ya fue creado en hacer_pedido
    
    if request.method == 'POST':
        # Formulario para actualizar el pago
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.estado = "pagado"  # Marcar como pagado
            pago.save()
            return redirect('pedidos:ver_pago', pago_id=pago.id)
    else:
        form = PagoForm(instance=pago)
    
    return render(request, 'pedidos/pagar_pedido.html', {'form': form, 'pedido': pedido})

# Ver el detalle del pago
@login_required
def ver_pago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id, pedido__usuario=request.user)
    return render(request, 'pedidos/ver_pago.html', {'pago': pago})


# ---------------- Vistas de administración ---------------- #

# Cambiar el estado de un pedido (ej: pendiente → procesado)
@staff_member_required
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    valores_validos = [estado[0] for estado in Pedido.ESTADOS]

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

# Cambiar el estado de un pago (ej: pendiente → pagado)
@staff_member_required
def cambiar_estado_pago(request, pago_id, nuevo_estado):
    pago = get_object_or_404(Pago, id=pago_id)
    try:
        pago.cambiar_estado(nuevo_estado)
        messages.success(request, f"El estado del pago {pago.id} cambió a {nuevo_estado}.")
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('detalle_pedido', pedido_id=pago.pedido.id)

# Lista de todos los pedidos (solo admin)
def lista_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

# Lista de pedidos del usuario logueado
@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, "pedidos/mis_pedidos.html", {"pedidos": pedidos})


# ---------------- Exportaciones ---------------- #

# Generar un PDF con el detalle de un pedido
@login_required
def pedido_pdf(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    template = get_template("pedidos/pedido_pdf.html")  # Plantilla para el PDF
    html = template.render({"pedido": pedido})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="pedido_{pedido.id}.pdf"'

    # Crear el PDF con xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)
    
    return response

# Exportar pedidos pagados a un archivo Excel
@staff_member_required
def exportar_pedidos_pagados_excel(request):
    # Filtrar solo pedidos cuyo pago está marcado como pagado
    pedidos = Pedido.objects.filter(pago__estado="pagado")

    # Crear libro y hoja de Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pedidos Pagados"

    # Encabezados de la tabla
    ws.append(["ID", "Cliente", "Dirección", "Fecha", "Total", "Estado Pedido", "Productos"])

    # Agregar cada pedido como fila
    for pedido in pedidos:
        productos_str = ", ".join(
            [f"{item.producto} x{item.cantidad}" for item in pedido.items.all()]
        )
        ws.append([
            pedido.id,
            pedido.usuario.nombre,
            getattr(pedido.usuario, "direccion", "N/A"),  # Dirección opcional
            pedido.fecha.strftime("%Y-%m-%d %H:%M"),
            float(pedido.total),
            pedido.estado,
            productos_str
        ])

    # Respuesta HTTP con el archivo Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="pedidos_pagados.xlsx"'
    wb.save(response)
    return response
