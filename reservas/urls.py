#Realizado por Mariana Valderrama
from django.urls import path
from . import views


app_name = 'reservas'

urlpatterns = [
    # URLs para reservas
    path('', views.lista_reservas, name='lista_reservas'),
    path('crear/', views.manejar_reserva, name='manejar_reserva'),
    path('<int:reserva_id>/editar/', views.manejar_reserva, name='editar_reserva'),
    path('eliminar/<int:reserva_id>/', views.eliminar_reserva, name='eliminar_reserva'),
    path('planes/', views.planes, name='planes'),
   
]
