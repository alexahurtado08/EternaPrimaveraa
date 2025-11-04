from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistroUsuarioTests(TestCase):
    def test_registro_usuario_exitoso(self):
        """
        Debe crear un usuario nuevo y redirigir al login.
        """
        url = reverse('usuarios:registrar_usuario')  # nombre de tu ruta
        datos = {
            'correo': 'nuevo@usuario.com',
            'nombre': 'Nuevo Usuario',
            'telefono': '1234567890',
            'direccion': 'Calle 123',
            'password': '12345',
        }
        response = self.client.post(url, datos)

        # Debe redirigir al login
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuarios:login_usuario'))

        # Verificar que se creó el usuario
        usuario = User.objects.filter(correo='nuevo@usuario.com').first()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, 'Nuevo Usuario')

        # Verificar que la contraseña esté encriptada
        self.assertTrue(usuario.check_password('12345'))

    def test_registro_usuario_con_errores(self):
        """
        Debe mostrar errores si falta algún campo obligatorio.
        """
        url = reverse('usuarios:registrar_usuario')
        datos_incorrectos = {
            'correo': '',  # correo vacío
            'nombre': 'Usuario',
            'telefono': '1234567890',
            'direccion': 'Calle 123',
            'password': '12345',
        }
        response = self.client.post(url, datos_incorrectos)

        # No debe redirigir, debe mostrar la misma página
        self.assertEqual(response.status_code, 200)

        # Verificar que no se creó ningún usuario
        self.assertFalse(User.objects.filter(nombre='Usuario').exists())
