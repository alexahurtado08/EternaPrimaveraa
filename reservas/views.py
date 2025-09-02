#Realizado por Mariana Valderrama
from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from .forms import ReservaForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Reserva
from datetime import datetime

# views.py
from django.shortcuts import render
from .models import Reserva

from django.shortcuts import render
from .models import Reserva


def lista_reservas(request):
    reservas = Reserva.objects.all()

    # Obtenemos los parámetros de búsqueda desde el formulario
    fecha_llegada = request.GET.get("fecha_llegada")
    personas = request.GET.get("personas")
    plan = request.GET.get("plan")

    # Filtrar por fecha de llegada exacta (no contiene, sino igualdad)
    if fecha_llegada:
        reservas = reservas.filter(fecha_llegada=fecha_llegada)

    # Filtrar por cantidad de personas exacta
    if personas:
        reservas = reservas.filter(numero_personas=personas)

    # Filtrar por plan
    if plan:
        reservas = reservas.filter(tipo_plan=plan)

    return render(request, "reservas/lista_reservas.html", {
        "reservas": reservas
    })



@login_required(login_url='usuarios:login_usuario')
def crear_reserva(request):
    """
    Permite crear una nueva reserva usando ReservaForm.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'reservas/confirmacion_reserva.html')
    else:
        form = ReservaForm()
    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required(login_url='usuarios:login_usuario')
def editar_reserva(request, reserva_id):
    """
    Edita una reserva existente.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('reservas:lista_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/crear_reserva.html', {'form': form})

@login_required(login_url='usuarios:login_usuario')
def eliminar_reserva(request, reserva_id):
    """
    Elimina una reserva.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    return redirect('reservas:lista_reservas')


def planes(request):
    return render(request, 'planes/plan.html')
