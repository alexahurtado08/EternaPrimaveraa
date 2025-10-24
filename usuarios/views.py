# Realizado por Mariana Valderrama
# usuarios/views.py

from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from pedidos.models import Pedido, Pago
from producto.models import Producto


# -------------------------------
# Registro de usuario
# -------------------------------
def registrar_usuario(request):
    """
    Vista para registrar un nuevo usuario.
    - Se encripta la contraseña antes de guardar.
    - Tras el registro, se redirige al login.
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)  # no guardar aún
            usuario.set_password(form.cleaned_data['password'])  # encriptar
            usuario.save()  # guardar en DB
            return redirect('usuarios:login_usuario')
    else:
        form = UsuarioForm()
    
    return render(request, 'usuarios/registrar_usuario.html', {'form': form})


# -------------------------------
# Listado de usuarios (vista simple)
# -------------------------------
def lista_usuarios(request):
    """
    Vista para mostrar todos los usuarios registrados.
    """
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


# -------------------------------
# Login de usuario
# -------------------------------
def login_usuario(request):
    """
    Vista para iniciar sesión:
    - Autentica con correo y contraseña.
    - Si es superusuario → redirige al panel admin.
    - Si es usuario normal → redirige al home.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            password = form.cleaned_data["password"]
            user = authenticate(request, correo=correo, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:  # redirección condicional
                    return redirect("usuarios:admin_home")
                return redirect("home")
            else:
                form.add_error(None, "❌ Correo o contraseña incorrectos")
    else:
        form = LoginForm()

    return render(request, "usuarios/login.html", {"form": form})


# -------------------------------
# Logout
# -------------------------------
def logout_usuario(request):
    """
    Cierra la sesión del usuario y lo redirige al login.
    """
    logout(request)
    return redirect("usuarios:login_usuario")


# -------------------------------
# Home exclusivo para superusuarios
# -------------------------------
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    """
    Página inicial del superusuario con dashboard incluido.
    """
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()

    pedidos_por_estado = Pedido.objects.values("estado").annotate(total=Count("id"))
    pagos_por_estado = Pago.objects.values("estado").annotate(total=Count("id"))
    total_pagos = Pago.objects.aggregate(total=Sum("total"))["total"] or 0

    contexto = {
        "total_usuarios": total_usuarios,
        "total_productos": total_productos,
        "total_pedidos": total_pedidos,
        "pedidos_por_estado": pedidos_por_estado,
        "total_pagos": total_pagos,
        "pagos_por_estado": pagos_por_estado,
    }
    return render(request, "usuarios/admin_home.html", contexto)



# -------------------------------
# Dashboard administrativo
# -------------------------------
@staff_member_required
def dashboard_admin(request):
    """
    Panel de control para staff:
    - Muestra métricas generales:
        * Total de usuarios
        * Total de productos
        * Total de pedidos
        * Pedidos agrupados por estado
        * Pagos totales
        * Pagos agrupados por estado
    """
    # Totales básicos
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()

    # Agrupaciones
    pedidos_por_estado = Pedido.objects.values("estado").annotate(total=Count("id"))
    pagos_por_estado = Pago.objects.values("estado").annotate(total=Count("id"))

    # Suma total de pagos recibidos
    total_pagos = Pago.objects.aggregate(total=Sum("total"))["total"] or 0

    contexto = {
        "total_usuarios": total_usuarios,
        "total_productos": total_productos,
        "total_pedidos": total_pedidos,
        "pedidos_por_estado": pedidos_por_estado,
        "total_pagos": total_pagos,
        "pagos_por_estado": pagos_por_estado,
    }
    return render(request, "usuarios/dashboard_admin.html", contexto)
