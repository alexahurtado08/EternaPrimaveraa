# Dockerfile para EternaPrimaveraa (Django con Gunicorn)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gettext \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 8000

# Ejecuta Gunicorn directamente sin entrypoint
CMD ["gunicorn", "EternaPrimavera.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
