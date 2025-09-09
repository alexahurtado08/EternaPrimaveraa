# views.py
# Realizado por Mariana Valderrama
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Reserva
from .forms import ReservaForm

@login_required(login_url='usuarios:login_usuario')
def lista_reservas(request):
    reservas = Reserva.objects.all()

    # Filtros simples por GET
    fecha_llegada = request.GET.get("fecha_llegada")
    personas = request.GET.get("personas")
    plan = request.GET.get("plan")

    if fecha_llegada:
        reservas = reservas.filter(fecha_llegada=fecha_llegada)
    if personas:
        reservas = reservas.filter(numero_personas=personas)
    if plan:
        reservas = reservas.filter(tipo_plan=plan)

    return render(request, "reservas/lista_reservas.html", {"reservas": reservas})


@login_required(login_url='usuarios:login_usuario')
@login_required(login_url='usuarios:login_usuario')
def manejar_reserva(request, reserva_id=None):
    reserva = get_object_or_404(Reserva, id=reserva_id) if reserva_id else None

    # Solo admin puede editar
    if reserva and not request.user.is_staff:
        messages.error(request, "No tienes permisos para editar reservas.")
        return redirect('reservas:lista_reservas')

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)
            if not reserva:  # si es nueva reserva
                nueva_reserva.usuario = request.user
            nueva_reserva.save()

            if not reserva:  
                # Si es creación, mostrar confirmación
                return render(request, "reservas/confirmacion_reserva.html", {
                    "reserva": nueva_reserva
                })
            else:
                # Si es edición, redirigir al listado
                messages.success(request, "✅ Reserva actualizada correctamente.")
                return redirect('reservas:lista_reservas')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, "reservas/form_reserva.html", {
        'form': form,
        'es_edicion': bool(reserva)
    })



@login_required(login_url='usuarios:login_usuario')
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    messages.success(request, f"❌ Reserva {reserva.id} eliminada.")
    return redirect('reservas:lista_reservas')


def planes(request):
    return render(request, 'planes/plan.html')
