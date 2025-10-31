# Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _  # ✅ Import para traducciones
from django.utils import timezone
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from producto.models import Producto
from carrito.models import Carrito
from .models import Pedido, Pago, PedidoItem
from .forms import PagoForm
from .services.pdf_report_generator import PDFReportGenerator
from .services.excel_report_generator import ExcelReportGenerator


# ---------------- Vistas de usuario ---------------- #

@login_required
def hacer_pedido(request):
    """Crea un pedido a partir del carrito actual."""
    carrito = Carrito.objects.get(usuario=request.user)
    items = carrito.items.all()

    if not items:
        messages.warning(request, _("Tu carrito está vacío."))
        return redirect("carrito:ver_carrito")

    pedido = Pedido.objects.create(
        usuario=request.user,
        fecha=timezone.now(),
        total=sum(item.producto.precio * item.cantidad for item in items),
        estado=_("pendiente")  # 🔹 Estado traducible
    )

    for item in items:
        PedidoItem.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio=item.producto.precio
        )

    Pago.objects.create(
        pedido=pedido,
        metodo=_("efectivo"),
        total=pedido.total,
        estado=_("pendiente")
    )

    items.delete()
    messages.success(request, _("Pedido creado correctamente."))
    return redirect("pedidos:detalle_pedido", pedido_id=pedido.id)


@login_required
def detalle_pedido(request, pedido_id):
    """Muestra el detalle de un pedido del usuario."""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "pedidos/detalle_pedido.html", {"pedido": pedido})


@login_required
def pagar_pedido(request, pedido_id):
    """Permite realizar o actualizar el pago de un pedido."""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    pago = pedido.pago

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.estado = _("pagado")  # 🔹 Traducción del estado
            pago.save()
            messages.success(request, _("Pago realizado exitosamente."))
            return redirect('pedidos:ver_pago', pago_id=pago.id)
    else:
        form = PagoForm(instance=pago)

    return render(request, 'pedidos/pagar_pedido.html', {'form': form, 'pedido': pedido})


@login_required
def ver_pago(request, pago_id):
    """Muestra los detalles del pago realizado."""
    pago = get_object_or_404(Pago, id=pago_id, pedido__usuario=request.user)
    return render(request, 'pedidos/ver_pago.html', {'pago': pago})


# ---------------- Vistas de administración ---------------- #

@staff_member_required
def cambiar_estado_pedido(request, pedido_id, nuevo_estado):
    """Cambia el estado de un pedido (solo admin)."""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    valores_validos = [estado[0] for estado in Pedido.ESTADOS]

    if nuevo_estado in valores_validos:
        pedido.estado = nuevo_estado
        pedido.save()
        messages.success(
            request,
            _("El estado del pedido %(pedido_id)s cambió a %(estado)s.") % {
                "pedido_id": pedido.id,
                "estado": pedido.get_estado_display()
            }
        )
    else:
        messages.error(request, _("Estado no válido."))
    return redirect('pedidos:lista_pedidos')


@staff_member_required
def cambiar_estado_pago(request, pago_id, nuevo_estado):
    """Cambia el estado de un pago (solo admin)."""
    pago = get_object_or_404(Pago, id=pago_id)
    try:
        pago.cambiar_estado(nuevo_estado)
        messages.success(
            request,
            _("El estado del pago %(pago_id)s cambió a %(estado)s.") % {
                "pago_id": pago.id,
                "estado": nuevo_estado
            }
        )
    except ValueError as e:
        messages.error(request, str(e))
    return redirect('detalle_pedido', pedido_id=pago.pedido.id)


def lista_pedidos(request):
    """Lista de todos los pedidos (admin)."""
    pedidos = Pedido.objects.all()
    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})


@login_required
def mis_pedidos(request):
    """Lista de pedidos del usuario actual."""
    pedidos = Pedido.objects.filter(usuario=request.user)
    return render(request, "pedidos/mis_pedidos.html", {"pedidos": pedidos})


# ---------------- Exportaciones ---------------- #

@login_required
def pedido_pdf(request, pedido_id):
    """Genera un reporte PDF del pedido."""
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    report_generator = PDFReportGenerator()
    context = {"pedido": pedido}
    return report_generator.generate("pedidos/pedido_pdf.html", context, f"pedido_{pedido.id}")


@staff_member_required
def exportar_pedidos_pagados_excel(request):
    """Exporta los pedidos pagados a Excel."""
    pedidos = Pedido.objects.filter(pago__estado="pagado")
    report_generator = ExcelReportGenerator()
    return report_generator.generate(pedidos, "pedidos_pagados")
