# Realizado por [Tu nombre]
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _  # ✅ Import para traducciones
import requests

def obtener_clima():
    """Consulta el clima actual en Barbosa usando OpenWeather API"""
    ciudad = "Barbosa"
    api_key = "38f5bc8bc3fa7910b0d9742cb2054c14"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"

    try:
        response = requests.get(url, timeout=5)
        clima = response.json()
        print("🌦️ Respuesta de la API:", clima)

        if response.status_code == 200 and "main" in clima:
            temperatura = clima["main"]["temp"]
            descripcion = clima["weather"][0]["description"].capitalize()
        else:
            print("⚠️ Error en la API:", clima)
            temperatura = None
            # 🔹 Texto traducible
            descripcion = _("No disponible")
    except Exception as e:
        print("⚠️ Error al conectar con la API:", e)
        temperatura = None
        # 🔹 Texto traducible
        descripcion = _("Error al obtener el clima")

    # 🔹 Todos los textos devueltos deben poder traducirse
    return {
        "temperatura": temperatura,
        "descripcion": descripcion,
        "ciudad": _(ciudad),  # Por si quieres traducir el nombre de la ciudad también
    }

@login_required
def home(request):
    contexto = obtener_clima()
    return render(request, 'home.html', contexto)
