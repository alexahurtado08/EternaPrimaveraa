from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from pedidos.models import Pedido, Pago
from carrito.models import Carrito, ItemCarrito
from producto.models import Producto

class HacerPedidoTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            correo='alex@example.com',   # o el campo que tu modelo use como identificador
            nombre='Alex',
            password='123'
        )
        self.client.login(correo='alex@example.com', password='123')


        # 🔹 Crear el carrito del usuario
        self.carrito = Carrito.objects.create(usuario=self.user)

        # 🔹 Crear un producto de prueba
        self.producto = Producto.objects.create(
            nombre='Jabón artesanal',
            precio=10000,
            descripcion='Jabón natural con miel',
            cantidad=10  # obligatorio según tu modelo
        )

        # 🔹 Crear un item en el carrito
        self.item = ItemCarrito.objects.create(
            carrito=self.carrito,
            producto=self.producto,
            cantidad=2
        )

    def test_crear_pedido_exitoso(self):
        # Usar reverse si tienes nombre de ruta definido, si no la URL directa
        url = reverse('pedidos:hacer_pedido')  # Ajusta el nombre de la ruta
        response = self.client.get(url)

        # Verificar redirección
        self.assertEqual(response.status_code, 302)

        # Verificar que se creó el pedido
        pedido = Pedido.objects.filter(usuario=self.user).first()
        self.assertIsNotNone(pedido)
        self.assertEqual(float(pedido.total), 20000)  # 10000*2

        # Verificar que se creó el pago
        pago = Pago.objects.filter(pedido=pedido).first()
        self.assertIsNotNone(pago)
        self.assertEqual(float(pago.total), 20000)
        self.assertEqual(pago.estado, 'pendiente')

        # Verificar que el carrito quedó vacío
        self.assertEqual(self.carrito.items.count(), 0)
