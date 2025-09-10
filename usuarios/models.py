# Realizado por Mariana Valderrama
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models


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
            raise ValueError("El usuario debe tener un correo electrónico")
        
        correo = self.normalize_email(correo)  # normalizar correo
        usuario = self.model(correo=correo, nombre=nombre, **extra_fields)
        usuario.set_password(password)  # encriptar contraseña
        usuario.save(using=self._db)    # guardar en BD
        return usuario

    def create_superuser(self, correo, nombre, password=None, **extra_fields):
        """
        Crea un superusuario (admin).
        - Asegura que is_staff y is_superuser estén en True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("El superusuario debe tener is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("El superusuario debe tener is_superuser=True.")

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

    id = models.AutoField(primary_key=True)  # ID único
    nombre = models.CharField(max_length=100)  # Nombre completo
    correo = models.EmailField(unique=True)    # Correo único (se usa para login)
    telefono = models.CharField(max_length=15, blank=False, null=False)  # Teléfono obligatorio
    direccion = models.TextField(blank=False, null=False)  # Dirección obligatoria
    
    # Campos de control
    is_active = models.BooleanField(default=True)   # Activo o no
    is_staff = models.BooleanField(default=False)   # Acceso al admin

    # Manager personalizado
    objects = UsuarioManager()

    # Campo usado como "username" en la autenticación
    USERNAME_FIELD = "correo"
    REQUIRED_FIELDS = ["nombre"]  # Campo extra obligatorio al crear superusuarios

    def __str__(self):
        # Representación legible del usuario
        return f"{self.nombre} ({self.correo})"
