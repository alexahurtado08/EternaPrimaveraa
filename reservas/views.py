# views.py
# Realizado por Mariana Valderrama
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext as _  # ✅ Import para traducción
from .models import Reserva
from .forms import ReservaForm


# Vista para listar todas las reservas con posibilidad de aplicar filtros
@login_required(login_url='usuarios:login_usuario')
def lista_reservas(request):
    reservas = Reserva.objects.all()

    # Filtros simples desde la URL (GET parameters)
    fecha_llegada = request.GET.get("fecha_llegada")
    personas = request.GET.get("personas")
    plan = request.GET.get("plan")

    # Aplicación de filtros si existen parámetros
    if fecha_llegada:
        reservas = reservas.filter(fecha_llegada=fecha_llegada)
    if personas:
        reservas = reservas.filter(numero_personas=personas)
    if plan:
        reservas = reservas.filter(tipo_plan=plan)

    # Renderizamos la lista filtrada de reservas
    return render(request, "reservas/lista_reservas.html", {
        "reservas": reservas,
        "titulo": _("Lista de reservas"),  # ✅ Texto traducible
    })


# Vista para crear o editar una reserva
@login_required(login_url='usuarios:login_usuario')
def manejar_reserva(request, reserva_id=None):
    reserva = get_object_or_404(Reserva, id=reserva_id) if reserva_id else None

    # Solo el administrador puede editar reservas existentes
    if reserva and not request.user.is_staff:
        messages.error(request, _("No tienes permisos para editar reservas."))
        return redirect('reservas:lista_reservas')

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)

            if not reserva:
                nueva_reserva.usuario = request.user
            nueva_reserva.save()

            if not reserva:
                # ✅ Traducción del texto mostrado en confirmación
                messages.success(request, _("Reserva creada exitosamente."))
                return render(request, "reservas/confirmacion_reserva.html", {
                    "reserva": nueva_reserva,
                    "mensaje": _("Tu reserva fue registrada correctamente."),
                })
            else:
                messages.success(request, _("Reserva actualizada correctamente."))
                return redirect('reservas:lista_reservas')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, "reservas/form_reserva.html", {
        'form': form,
        'es_edicion': bool(reserva),
        'titulo': _("Editar Reserva") if reserva else _("Nueva Reserva"),
    })


# Vista para eliminar una reserva
@login_required(login_url='usuarios:login_usuario')
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)

    # 🔒 Solo el dueño o un administrador pueden eliminar
    if reserva.usuario != request.user and not request.user.is_staff:
        messages.error(request, _("No tienes permiso para eliminar esta reserva."))
        return redirect('reservas:lista_reservas')

    reserva.delete()
    messages.success(request, _("Reserva eliminada correctamente."))
    return redirect('reservas:lista_reservas')


# Vista simple para mostrar planes
def planes(request):
    return render(request, 'planes/plan.html', {
        "titulo": _("Nuestros Planes Turísticos")
    })
