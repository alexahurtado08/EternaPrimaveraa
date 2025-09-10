# Realizado por Alexandra Hurtado
from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm

# ---------------- Vistas de Productos ---------------- #

# Vista para mostrar todos los productos disponibles
def lista_productos(request):
    # Obtiene todos los productos de la base de datos
    productos = Producto.objects.all()
    # Renderiza la lista de productos en la plantilla correspondiente
    return render(request, 'producto/lista_productos.html', {'productos': productos})

# Vista para mostrar el detalle de un producto específico
def detalle_producto(request, producto_id):
    # Busca el producto por su ID, si no existe lanza error 404
    producto = get_object_or_404(Producto, id=producto_id)
    # Renderiza el detalle del producto en la plantilla
    return render(request, 'producto/detalle_producto.html', {'producto': producto})

# Vista para crear un nuevo producto
def crear_producto(request):
    if request.method == 'POST':
        # Si el formulario fue enviado, lo cargamos con datos y archivos (ej: imágenes)
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardamos el nuevo producto en la base de datos
            form.save()
            return redirect('producto:lista_productos')  # Redirige a la lista de productos
    else:
        # Si es GET, mostramos el formulario vacío
        form = ProductoForm()
    
    # Renderiza la plantilla con el formulario
    return render(request, 'producto/formulario_producto.html', {'form': form})
