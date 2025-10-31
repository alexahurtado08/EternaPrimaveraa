from .views import obtener_clima

def clima_context(request):
    clima_data = obtener_clima()
    return {'clima_data': clima_data}
