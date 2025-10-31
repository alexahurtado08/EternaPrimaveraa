# Realizado por Mariana Valderrama
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


# -------------------------------
# Manager personalizado de Usuario
# -------------------------------
class UsuarioManager(BaseUserManager):
    """
    Manager que define cómo crear usuarios y superusuarios.
    """

    def create_user(self, correo, nombre, password=None, **extra_fields):
        """
        Crea un usuario normal con correo y nombre obligatorios.
        - Valida que el correo no esté vacío.
        - Normaliza el correo (minúsculas).
        - Encripta la contraseña.
        """
        if not correo:
            raise ValueError(_("El usuario debe tener un correo electrónico"))
        
        correo = self.normalize_email(correo)
        usuario = self.model(correo=correo, nombre=nombre, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        """
        Crea un superusuario (admin).
        - Asegura que is_staff y is_superuser estén en True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("El superusuario debe tener is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("El superusuario debe tener is_superuser=True."))

        return self.create_user(correo, nombre, password, **extra_fields)


# -------------------------------
# Modelo de Usuario personalizado
# -------------------------------
class Usuario(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado que reemplaza al User de Django.
    - Usa correo en lugar de username.
    - Incluye datos básicos: nombre, correo, teléfono y dirección.
    """

    id = models.AutoField(primary_key=True, verbose_name=_("ID de usuario"))
    nombre = models.CharField(max_length=100, verbose_name=_("nombre completo"))
    correo = models.EmailField(unique=True, verbose_name=_("correo electrónico"))
    telefono = models.CharField(
        max_length=15,
        blank=False,
        null=False,
        verbose_name=_("teléfono"),
        help_text=_("Número de contacto del usuario"),
    )
    direccion = models.TextField(
        blank=False,
        null=False,
        verbose_name=_("dirección"),
        help_text=_("Dirección de residencia del usuario"),
    )

    # Campos de control
    is_active = models.BooleanField(default=True, verbose_name=_("activo"))
    is_staff = models.BooleanField(default=False, verbose_name=_("miembro del staff"))

    # Manager personalizado
    objects = UsuarioManager()

    # Campo usado como "username" en la autenticación
    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre"]

    class Meta:
        verbose_name = _("usuario")
        verbose_name_plural = _("usuarios")

    def __str__(self):
        # Representación legible del usuario
        return f"{self.nombre} ({self.correo})"
