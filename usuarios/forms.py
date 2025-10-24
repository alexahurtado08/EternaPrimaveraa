# Realizado por Mariana Valderrama
from django import forms
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
        label="Contraseña"
    )

    class Meta:
        model = Usuario
        # Campos que se mostrarán en el formulario
        fields = ['nombre', 'correo', 'password', 'telefono', 'direccion']
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
    correo = forms.EmailField(label="Correo")
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña"
    )
