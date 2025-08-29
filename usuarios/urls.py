from django.urls import path
from usuarios import views

app_name = "usuarios" 
urlpatterns = [
    path('lista_usuarios', views.lista_usuarios, name='lista_usuarios'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path("login/", views.login_usuario, name="login_usuario"),
    path("logout/", views.logout_usuario, name="logout_usuario"),
]
