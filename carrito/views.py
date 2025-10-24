# Realizado por Alexandra Hurtado
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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
    # Busca el producto, si no existe devuelve error 404
    producto = get_object_or_404(Producto, id=producto_id)
    # Obtiene el carrito del usuario
    carrito = obtener_carrito(request.user)

    if request.method == "POST":
        # Obtiene la cantidad del formulario (por defecto 1 si no viene en la petición)
        cantidad = int(request.POST.get("cantidad", 1))
        # Busca si ya existe ese producto en el carrito
        item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not creado:
            # Si ya existe, suma la nueva cantidad
            item.cantidad += cantidad
        else:
            # Si es nuevo, asigna la cantidad inicial
            item.cantidad = cantidad
        item.save()  # Guarda el item en la base de datos
    # Redirige a la vista del carrito
    return redirect("carrito:ver_carrito")

# Vista para mostrar el carrito del usuario
@login_required(login_url='usuarios:login_usuario')
def ver_carrito(request):
    carrito = obtener_carrito(request.user)  # Obtiene el carrito del usuario
    # Renderiza la plantilla del carrito con el objeto carrito
    return render(request, "carrito/ver_carrito.html", {"carrito": carrito})

# Vista para eliminar un producto específico del carrito
@login_required(login_url='usuarios:login_usuario')
def eliminar_item(request, item_id):
    # Busca el item en el carrito del usuario, si no existe lanza error 404
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()  # Elimina el item
    return redirect("carrito:ver_carrito")  # Redirige a la vista del carrito

# Vista para actualizar la cantidad de un producto en el carrito
@login_required(login_url='usuarios:login_usuario')
def actualizar_cantidad(request, item_id):
    # Obtiene el item dentro del carrito del usuario
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

    if request.method == "POST":
        form = CantidadItemForm(request.POST)  # Formulario para validar la cantidad
        if form.is_valid():
            # Actualiza la cantidad con el valor ingresado
            item.cantidad = form.cleaned_data['cantidad']
            item.save()
    # Redirige a la vista del carrito
    return redirect("carrito:ver_carrito")
