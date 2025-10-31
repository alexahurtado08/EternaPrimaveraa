# Realizado por Alexandra Hurtado
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Producto
from .forms import ProductoForm


# ---------------- Vistas de Productos ---------------- #

# Vista para mostrar todos los productos disponibles
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto/lista_productos.html', {'productos': productos})


# Vista para mostrar el detalle de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto/detalle_producto.html', {'producto': producto})


# 🔒 Solo superusuarios pueden crear productos
@user_passes_test(lambda u: u.is_superuser)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto:lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'producto/formulario_producto.html', {'form': form, 'accion': 'Crear Producto'})


# 🔒 Solo superusuarios pueden editar productos
@user_passes_test(lambda u: u.is_superuser)
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto/formulario_producto.html', {'form': form, 'accion': 'Editar Producto'})


# 🔒 Solo superusuarios pueden eliminar productos
@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto:lista_productos')
    return render(request, 'producto/confirmar_eliminar.html', {'producto': producto})
