# usuarios/views.py
from django.shortcuts import render, redirect
from .models import Usuario
from .forms import UsuarioForm, LoginForm
from django.contrib.auth import authenticate, login, logout

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']
            telefono = form.cleaned_data.get('telefono', '')
            direccion = form.cleaned_data.get('direccion', '')

            Usuario.objects.create_user(
                nombre=nombre,
                correo=correo,
                contrasena=password,
                telefono=telefono,
                direccion=direccion
            )
            # <-- Aquí usamos el namespace completo
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
                # Redirige al home del proyecto principal
                return redirect("home")
            else:
                form.add_error(None, "Correo o contraseña incorrectos")
    else:
        form = LoginForm()
    return render(request, "usuarios/login.html", {"form": form})


def logout_usuario(request):
    logout(request)
    return redirect("usuarios:login_usuario")
