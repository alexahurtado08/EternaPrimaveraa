#Realizado por Alexandra Hurtado
from django.urls import path
from . import views

app_name = "carrito"

urlpatterns = [
    path("", views.ver_carrito, name="ver_carrito"),
    path("agregar/<int:producto_id>/", views.agregar_producto, name="agregar_producto"),
    path("eliminar/<int:item_id>/", views.eliminar_item, name="eliminar_item"),
    path("actualizar/<int:item_id>/", views.actualizar_cantidad, name="actualizar_cantidad"),
]
