#Realizado por Mariana Valderrama
from django.urls import path
from . import views


app_name = 'reservas'

urlpatterns = [
    # URLs para reservas
    path('', views.lista_reservas, name='lista_reservas'),
    path('crear/', views.crear_reserva, name='crear_reserva'),
    path('editar/<int:reserva_id>/', views.editar_reserva, name='editar_reserva'),
    path('eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('planes/', views.planes, name='planes'),
   
]
