from django.shortcuts import render
import requests
from django.contrib.auth.decorators import login_required


def obtener_clima():
    """Consulta el clima actual en Medellín usando OpenWeather API"""
    ciudad = "Barbosa"
    api_key = "38f5bc8bc3fa7910b0d9742cb2054c14"  # tu nueva API key
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
            descripcion = "No disponible"
    except Exception as e:
        print("⚠️ Error al conectar con la API:", e)
        temperatura = None
        descripcion = "Error al obtener clima"

    return {
        "temperatura": temperatura,
        "descripcion": descripcion,
        "ciudad": ciudad,
    }

@login_required
def home(request):
    contexto = obtener_clima()  # obtiene el clima y lo pasa al contexto
    return render(request, 'home.html', contexto)