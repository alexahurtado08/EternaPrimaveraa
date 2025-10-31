# usuarios/views.py
# Realizado por Mariana Valderrama

from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils.translation import gettext as _  # ✅ Traducción
from django.contrib import messages
from pedidos.models import Pedido, Pago
from producto.models import Producto


# -------------------------------
# Registro de usuario
# -------------------------------
def registrar_usuario(request):
    """
    Vista para registrar un nuevo usuario.
    """
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, _("Registro completado correctamente."))
            return redirect('usuarios:login_usuario')
        else:
            messages.error(request, _("Por favor, corrige los errores en el formulario."))
    else:
        form = UsuarioForm()
    
    return render(request, 'usuarios/registrar_usuario.html', {
        'form': form,
        'titulo': _("Registro de usuario"),
    })


# -------------------------------
# Listado de usuarios
# -------------------------------
def lista_usuarios(request):
    """
    Muestra todos los usuarios registrados.
    """
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {
        'usuarios': usuarios,
        'titulo': _("Lista de usuarios"),
    })


# -------------------------------
# Login de usuario
# -------------------------------
def login_usuario(request):
    """
    Vista para iniciar sesión.
    """
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            password = form.cleaned_data["password"]
            user = authenticate(request, correo=correo, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, _("Inicio de sesión exitoso."))
                if user.is_superuser:
                    return redirect("usuarios:admin_home")
                return redirect("home")
            else:
                form.add_error(None, _("❌ Correo o contraseña incorrectos."))
    else:
        form = LoginForm()

    return render(request, "usuarios/login.html", {
        "form": form,
        "titulo": _("Iniciar sesión"),
    })


# -------------------------------
# Logout
# -------------------------------
def logout_usuario(request):
    """
    Cierra la sesión y redirige al login.
    """
    logout(request)
    messages.info(request, _("Sesión cerrada correctamente."))
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
        "titulo": _("Panel de administración"),
        "descripcion": _("Resumen general del sistema."),
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
    Panel de control para personal administrativo.
    """
    total_usuarios = Usuario.objects.count()
    total_productos = Producto.objects.count()
    total_pedidos = Pedido.objects.count()

    pedidos_por_estado = Pedido.objects.values("estado").annotate(total=Count("id"))
    pagos_por_estado = Pago.objects.values("estado").annotate(total=Count("id"))
    total_pagos = Pago.objects.aggregate(total=Sum("total"))["total"] or 0

    contexto = {
        "titulo": _("Dashboard administrativo"),
        "descripcion": _("Métricas generales de usuarios, productos y pedidos."),
        "total_usuarios": total_usuarios,
        "total_productos": total_productos,
        "total_pedidos": total_pedidos,
        "pedidos_por_estado": pedidos_por_estado,
        "total_pagos": total_pagos,
        "pagos_por_estado": pagos_por_estado,
    }
    return render(request, "usuarios/dashboard_admin.html", contexto)
