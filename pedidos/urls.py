# pedidos/urls.py
from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path('hacer/', views.hacer_pedido, name='hacer_pedido'),
    path('pagar/<int:pedido_id>/', views.pagar_pedido, name='pagar_pedido'),
    path('pago/<int:pago_id>/', views.ver_pago, name='ver_pago'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('pedido/<int:pedido_id>/estado/<str:nuevo_estado>/',views.cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('pago/<int:pago_id>/estado/<str:nuevo_estado>/',views.cambiar_estado_pago, name='cambiar_estado_pago'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
]
