# Realizado por Mariana Valderrama
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ("id", "nombre", "correo", "telefono", "is_staff", "is_superuser")
    search_fields = ("nombre", "correo")
    ordering = ("correo",)
    list_filter = ("is_staff", "is_superuser", "is_active")

    # Campos visibles al editar un usuario
    fieldsets = (
        (None, {"fields": ("correo", "password")}),
        (_("Información personal"), {"fields": ("nombre", "telefono", "direccion")}),
        (_("Permisos"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Fechas importantes"), {"fields": ("last_login",)}),
    )

    # Campos visibles al crear un usuario desde el admin
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("correo", "nombre", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )
