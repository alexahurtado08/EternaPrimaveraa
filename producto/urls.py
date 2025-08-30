#Realizado por Alexandra Hurtado
from django.urls import path
from . import views

app_name = "producto"

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('nuevo/', views.crear_producto, name='crear_producto'),
]