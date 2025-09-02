
# Realizado por Alexandra Hurtado y Mariana Valderrama

from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal

from usuarios.models import Usuario
from producto.models import Producto
from pedidos.models import Pedido, PedidoItem, Pago
from carrito.models import Carrito, ItemCarrito
from reservas.models import Reserva

fake = Faker("es_ES")

class Command(BaseCommand):
    help = "Poblar la base de datos con datos de prueba"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando seed..."))

        # --- Productos fijos ---
        Producto.objects.all().delete()
        miel_grande = Producto.objects.create(
            nombre="Miel grande",
            descripcion="Frasco de miel pura de 1kg",
            cantidad=1000,
            precio=Decimal("24000.00")
        )
        miel_pequena = Producto.objects.create(
            nombre="Miel pequeña",
            descripcion="Frasco de miel pura de 500g",
            cantidad=500,
            precio=Decimal("22000.00")
        )
        self.stdout.write(self.style.SUCCESS("Productos creados ✅"))

        # --- Usuarios ---
        Usuario.objects.all().delete()
        usuarios = []
        for _ in range(15):
            user = Usuario.objects.create_user(
                correo=fake.unique.email(),
                nombre=fake.name(),
                telefono=fake.phone_number(),
                direccion=fake.address(),
                password="123456"
            )
            usuarios.append(user)
        self.stdout.write(self.style.SUCCESS("Usuarios creados ✅"))

        # --- Carritos e items ---
        Carrito.objects.all().delete()
        for u in usuarios:
            carrito = Carrito.objects.create(usuario=u)
            producto = random.choice([miel_grande, miel_pequena])
            ItemCarrito.objects.create(
                carrito=carrito,
                producto=producto,
                cantidad=random.randint(1, 3)
            )
        self.stdout.write(self.style.SUCCESS("Carritos creados ✅"))

        # --- Pedidos, Items y Pagos ---
        Pedido.objects.all().delete()
        Pago.objects.all().delete()
        for u in usuarios:
            pedido = Pedido.objects.create(
                usuario=u,
                estado=random.choice(["pendiente", "procesado", "entregado"]),
                total=random.choice([miel_grande.precio, miel_pequena.precio])
            )
            PedidoItem.objects.create(
                pedido=pedido,
                producto=miel_grande.nombre if random.random() > 0.5 else miel_pequena.nombre,
                cantidad=random.randint(1, 2),
                precio=pedido.total
            )
            Pago.objects.create(
                pedido=pedido,
                metodo=random.choice(["tarjeta", "paypal", "efectivo"]),
                total=pedido.total,
                estado=random.choice(["pendiente", "pagado"])
            )
        self.stdout.write(self.style.SUCCESS("Pedidos y pagos creados ✅"))

        # --- Reservas ---
        Reserva.objects.all().delete()
        for _ in range(10):
            llegada = fake.date_this_year()
            salida = fake.date_between(start_date=llegada, end_date="+10d")
            Reserva.objects.create(
                fecha_llegada=llegada,
                fecha_salida=salida,
                numero_personas=random.randint(1, 5),
                tipo_plan=random.choice(["basico", "premium", "vip"])
            )
        self.stdout.write(self.style.SUCCESS("Reservas creadas ✅"))

        self.stdout.write(self.style.SUCCESS("Seed finalizado 🚀"))
