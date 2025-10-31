# Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _  # 🔹 Import para traducciones
from producto.models import Producto
from .models import Carrito, ItemCarrito
from .forms import CantidadItemForm

# Función para obtener o crear un carrito para el usuario actual
def obtener_carrito(usuario):
    carrito, creado = Carrito.objects.get_or_create(usuario=usuario)
    return carrito

# Vista para agregar un producto al carrito
@login_required(login_url='usuarios:login_usuario')  # Solo usuarios logueados pueden acceder
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
        # 🔹 Ejemplo de mensaje traducible (puedes activarlo si agregas mensajes)
        # messages.success(request, _("Producto agregado correctamente al carrito."))
    return redirect("carrito:ver_carrito")

# Vista para mostrar el carrito del usuario
@login_required(login_url='usuarios:login_usuario')
def ver_carrito(request):
    carrito = obtener_carrito(request.user)
    # 🔹 Ejemplo si deseas mostrar mensaje traducible
    # if not carrito.itemcarrito_set.exists():
    #     messages.info(request, _("Tu carrito está vacío."))
    return render(request, "carrito/ver_carrito.html", {"carrito": carrito})

# Vista para eliminar un producto específico del carrito
@login_required(login_url='usuarios:login_usuario')
def eliminar_item(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    # 🔹 Ejemplo de mensaje traducible
    # messages.success(request, _("Producto eliminado del carrito."))
    return redirect("carrito:ver_carrito")

# Vista para actualizar la cantidad de un producto en el carrito
@login_required(login_url='usuarios:login_usuario')
def actualizar_cantidad(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

    if request.method == "POST":
        form = CantidadItemForm(request.POST)
        if form.is_valid():
            item.cantidad = form.cleaned_data['cantidad']
            item.save()
            # 🔹 Ejemplo de mensaje traducible
            # messages.success(request, _("Cantidad actualizada correctamente."))
    return redirect("carrito:ver_carrito")
