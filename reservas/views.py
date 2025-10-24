# views.py
# Realizado por Mariana Valderrama
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
    return render(request, "reservas/lista_reservas.html", {"reservas": reservas})


# Vista para crear o editar una reserva
@login_required(login_url='usuarios:login_usuario')
def manejar_reserva(request, reserva_id=None):
    # Si viene con id → es edición, si no → es nueva
    reserva = get_object_or_404(Reserva, id=reserva_id) if reserva_id else None

    # Solo el administrador puede editar reservas existentes
    if reserva and not request.user.is_staff:
        messages.error(request, "No tienes permisos para editar reservas.")
        return redirect('reservas:lista_reservas')

    if request.method == 'POST':
        # Cargar datos en el formulario
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)

            if not reserva:  
                # Si es una reserva nueva, asignamos al usuario actual
                nueva_reserva.usuario = request.user
            nueva_reserva.save()

            if not reserva:  
                # Caso creación → mostrar confirmación
                return render(request, "reservas/confirmacion_reserva.html", {
                    "reserva": nueva_reserva
                })
            else:
                # Caso edición → mostrar mensaje y redirigir
                messages.success(request, "✅ Reserva actualizada correctamente.")
                return redirect('reservas:lista_reservas')
    else:
        # Si es GET → mostrar formulario vacío o con datos de la reserva
        form = ReservaForm(instance=reserva)

    return render(request, "reservas/form_reserva.html", {
        'form': form,
        'es_edicion': bool(reserva)  # True si es edición, False si es nueva
    })


# Vista para eliminar una reserva
@login_required(login_url='usuarios:login_usuario')
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    messages.success(request, f"❌ Reserva {reserva.id} eliminada.")
    return redirect('reservas:lista_reservas')


# Vista simple para mostrar planes
def planes(request):
    return render(request, 'planes/plan.html')
