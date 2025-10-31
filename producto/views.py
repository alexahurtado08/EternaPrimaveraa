# Realizado por Alexandra Hurtado
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _  # ✅ Import para traducción
from django.http import JsonResponse
from django.urls import reverse

from .models import Producto
from .forms import ProductoForm


# ---------------- Vistas de Productos ---------------- #

def lista_productos(request):
    """Muestra todos los productos disponibles."""
    productos = Producto.objects.all()
    return render(request, 'producto/lista_productos.html', {'productos': productos})


def detalle_producto(request, producto_id):
    """Muestra el detalle de un producto específico."""
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto/detalle_producto.html', {'producto': producto})


# 🔒 Solo superusuarios pueden crear productos
@user_passes_test(lambda u: u.is_superuser)
def crear_producto(request):
    """Permite crear un nuevo producto (solo admin)."""
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto:lista_productos')
    else:
        form = ProductoForm()
    return render(
        request,
        'producto/formulario_producto.html',
        {
            'form': form,
            'accion': _('Crear Producto')  # ✅ Texto traducible
        }
    )


# 🔒 Solo superusuarios pueden editar productos
@user_passes_test(lambda u: u.is_superuser)
def editar_producto(request, producto_id):
    """Permite editar un producto existente (solo admin)."""
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('producto:lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(
        request,
        'producto/formulario_producto.html',
        {
            'form': form,
            'accion': _('Editar Producto')  # ✅ Texto traducible
        }
    )


# 🔒 Solo superusuarios pueden eliminar productos
@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, producto_id):
    """Permite eliminar un producto existente (solo admin)."""
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('producto:lista_productos')
    return render(
        request,
        'producto/confirmar_eliminar.html',
        {
            'producto': producto,
            'titulo_confirmacion': _('Confirmar eliminación de producto'),  # ✅ Texto traducible
        }
    )


def api_productos(request):
    """API JSON con todos los productos."""
    productos = Producto.objects.all()
    data = [
        {
            'id': p.id,
            'nombre': p.nombre,
            'precio': p.precio,
            'cantidad': p.cantidad,
            'url_detalle': request.build_absolute_uri(reverse('producto:detalle_producto', args=[p.id]))
        }
        for p in productos
    ]
    return JsonResponse({'productos': data})
