from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto
from .forms import ProductoForm

 #Vista para mostrar todos los productos disponibles.
   
def lista_productos(request):
   
    productos = Producto.objects.all()
    return render(request, 'producto/lista_productos.html', {'productos': productos})

# Vista que muestra el detalle de un producto específico.
   
def detalle_producto(request, producto_id):
   
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto/detalle_producto.html', {'producto': producto})


 # Vista que permite crear un nuevo producto.
   
def crear_producto(request):
  
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'producto/formulario_producto.html', {'form': form})
