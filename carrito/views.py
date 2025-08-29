from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, ItemCarrito
from producto.models import Producto
from .forms import ItemCarritoForm



# Ver carrito del usuario
#@login_required
def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user)
    else:
        carrito = request.session.get('carrito', [])
    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito})



# Agregar producto al carrito

#@login_required
def agregar_producto(request, producto_id):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == 'POST':
        form = ItemCarritoForm(request.POST)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']

            # Si el producto ya está en el carrito, sumamos cantidad
            item, creado = ItemCarrito.objects.get_or_create(
                carrito=carrito, producto=producto,
                defaults={'cantidad': cantidad}
            )
            if not creado:
                item.cantidad += cantidad
                item.save()

            return redirect('ver_carrito')
    else:
        form = ItemCarritoForm()

    return render(request, 'carrito/agregar_producto.html', {'form': form, 'producto': producto})



# Eliminar producto del carrito

#@login_required
def eliminar_producto(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)

    if request.method == 'POST':
        item.delete()
        return redirect('ver_carrito')

    return render(request, 'carrito/eliminar_producto.html', {'item': item})


def obtener_carrito(request):
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        carrito, _ = Carrito.objects.get_or_create(session_key=request.session.session_key)
    return carrito