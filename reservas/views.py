from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva
from .forms import ReservaForm

def lista_reservas(request):
    """
    Muestra todas las reservas.
    """
    reservas = Reserva.objects.all()
    return render(request, 'reservas/lista_reservas.html', {'reservas': reservas})

def crear_reserva(request):
    """
    Permite crear una nueva reserva usando ReservaForm.
    """
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm()
    return render(request, 'reservas/crear_reserva.html', {'form': form})

def editar_reserva(request, reserva_id):
    """
    Edita una reserva existente.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')
    else:
        form = ReservaForm(instance=reserva)
    return render(request, 'reservas/crear_reserva.html', {'form': form})

def eliminar_reserva(request, reserva_id):
    """
    Elimina una reserva.
    """
    reserva = get_object_or_404(Reserva, id=reserva_id)
    reserva.delete()
    return redirect('lista_reservas')


def planes(request):
    return render(request, 'planes/plan.html')
