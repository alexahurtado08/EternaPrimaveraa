from django.urls import path
from . import views

urlpatterns = [
    # Rutas de pedidos
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedidos/crear/<int:producto_id>/', views.crear_pedido_desde_producto, name='crear_pedido_desde_producto'),

    # Rutas de pagos
    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/<int:pago_id>/', views.detalle_pago, name='detalle_pago'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
]
