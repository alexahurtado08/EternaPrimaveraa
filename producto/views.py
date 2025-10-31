# Realizado por Alexandra Hurtado
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm
from django.http import JsonResponse

# ---------------- Vistas de Productos ---------------- #

# Vista para mostrar todos los productos disponibles
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'producto/lista_productos.html', {'productos': productos})


# Vista para mostrar el detalle de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto/detalle_producto.html', {'producto': producto})


# Vista para crear un nuevo producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('producto:lista_productos')
    else:
        form = ProductoForm()
    
    # Renderiza la plantilla con el formulario
    return render(request, 'producto/formulario_producto.html', {'form': form})

def api_productos(request):
    productos = Producto.objects.all().values('id', 'nombre', 'precio', 'cantidad')
    data = list(productos)
    return JsonResponse({'productos': data})
