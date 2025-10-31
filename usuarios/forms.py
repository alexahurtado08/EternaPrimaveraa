# Realizado por Mariana Valderrama
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Usuario


# -------------------------------
# Formulario de Registro de Usuario
# -------------------------------
class UsuarioForm(forms.ModelForm):
    """
    Formulario basado en el modelo Usuario.
    Se utiliza para registrar nuevos usuarios en el sistema.
    """

    # Campo de contraseña con widget tipo PasswordInput (oculta texto ingresado)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=_("Contraseña")
    )

    class Meta:
        model = Usuario
        # Campos que se mostrarán en el formulario
        fields = ['nombre', 'correo', 'password', 'telefono', 'direccion']

        # Etiquetas traducibles
        labels = {
            'nombre': _('Nombre completo'),
            'correo': _('Correo electrónico'),
            'telefono': _('Número de teléfono'),
            'direccion': _('Dirección de residencia'),
        }

        # Textos de ayuda traducibles
        help_texts = {
            'correo': _('Introduce una dirección de correo válida.'),
            'telefono': _('Ejemplo: +57 3001234567'),
        }

        # Widgets personalizados para dar estilo con Bootstrap
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        """
        Sobrescribimos el constructor para asegurar
        que todos los campos sean obligatorios.
        """
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True


# -------------------------------
# Formulario de Login
# -------------------------------
class LoginForm(forms.Form):
    """
    Formulario simple de inicio de sesión.
    No depende directamente del modelo Usuario.
    """
    correo = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label=_("Contraseña")
    )
