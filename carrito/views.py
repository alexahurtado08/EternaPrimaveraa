#Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from producto.models import Producto
from .models import Carrito, ItemCarrito
from .forms import CantidadItemForm

# Obtener o crear carrito del usuario
def obtener_carrito(usuario):
    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    return carrito

# Vista para agregar producto al carrito
@login_required
def agregar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = obtener_carrito(request.user)

    if request.method == "POST":
        cantidad = int(request.POST.get("cantidad", 1))
        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not creado:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()
    return redirect("carrito:ver_carrito")

# Vista para ver carrito
@login_required
def ver_carrito(request):
    carrito = obtener_carrito(request.user)
    return render(request, "carrito/ver_carrito.html", {"carrito": carrito})

# Vista para eliminar item del carrito
@login_required
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect("carrito:ver_carrito")

# Vista para actualizar cantidad de un item en el carrito
@login_required
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

    if request.method == "POST":
        form = CantidadItemForm(request.POST)
        if form.is_valid():
            item.cantidad = form.cleaned_data['cantidad']
            item.save()
    return redirect("carrito:ver_carrito")