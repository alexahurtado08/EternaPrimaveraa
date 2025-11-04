# Imagen base ligera de Python
FROM python:3.10-slim

# Evitar pyc y habilitar logs inmediatos
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libcairo2-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libtiff5-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    git \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de la app
WORKDIR /app

# Copiar requirements.txt primero
COPY requirements.txt .

# Actualizar pip e instalar dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Exponer puerto para Gunicorn
EXPOSE 8000

# Comando para correr la app
CMD ["gunicorn", "EternaPrimavera.wsgi:application", "--bind", "0.0.0.0:8000"]
