#Realizado por Mariana Valderrama
# usuarios/views.py
from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils.timezone import now
from pedidos.models import Pedido, Pago, PedidoItem
from reservas.models import Reserva
from producto.models import Producto

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Crear el usuario pero sin guardarlo aún
            usuario = form.save(commit=False)
            
            # Encriptar la contraseña
            usuario.set_password(form.cleaned_data['password'])
            
            # Guardar en DB
            usuario.save()

            return redirect('usuarios:login_usuario')
    else:
        form = UsuarioForm()
    
    return render(request, 'usuarios/registrar_usuario.html', {'form': form})




def lista_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/lista_usuarios.html', {'usuarios': usuarios})


def login_usuario(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data["correo"]
            password = form.cleaned_data["password"]
            user = authenticate(request, correo=correo, password=password)
            if user is not None:
                login(request, user)
                # 🔹 Redirección condicional
                if user.is_superuser:
                    return redirect("usuarios:admin_home")
                return redirect("home")
            else:
                form.add_error(None, "Correo o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, "usuarios/login.html", {"form": form})

def logout_usuario(request):
    logout(request)
    return redirect("usuarios:login_usuario")



# ✅ Solo para superusuarios
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_home(request):
    return render(request, "usuarios/admin_home.html")



@staff_member_required
def dashboard_admin(request):
    # Total de usuarios
    total_usuarios = Usuario.objects.count()

    # Total de productos
    total_productos = Producto.objects.count()

    # Total de pedidos
    total_pedidos = Pedido.objects.count()

    # Pedidos por estado (ejemplo: entregado, pendiente, cancelado)
    pedidos_por_estado = Pedido.objects.values("estado").annotate(total=Count("id"))

    # Pagos recibidos (sumatoria de montos)
    total_pagos = Pago.objects.aggregate(total=Sum("total"))["total"] or 0

    # Pagos por estado (ejemplo: aprobado, pendiente, rechazado)
    pagos_por_estado = Pago.objects.values("estado").annotate(total=Count("id"))

    contexto = {
        "total_usuarios": total_usuarios,
        "total_productos": total_productos,
        "total_pedidos": total_pedidos,
        "pedidos_por_estado": pedidos_por_estado,
        "total_pagos": total_pagos,
        "pagos_por_estado": pagos_por_estado,
    }
    return render(request, "usuarios/dashboard_admin.html", contexto)

