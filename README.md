#  Eterna Primavera - Plataforma E-commerce y Reservas

##  Descripción del proyecto
El proyecto busca desarrollar una plataforma de **e-commerce** para un emprendimiento familiar ubicado en **Barbosa**, que se dedica a la **producción de miel de abejas** y a la realización de **recorridos turísticos en su finca**.  

La solución permitirá que los clientes puedan:
- Comprar miel de forma sencilla a través de un **carrito de compras en línea**.
- Realizar **reservas digitales** para visitas guiadas, donde se muestra el proceso de producción de la miel y se promueve la **educación ambiental sobre la apicultura**.

---

##  Requisitos previos
- **Python 3.11+** instalado
- **Git** instalado

---

##  Clonar repositorio
```bash
git clone https://github.com/alexahurtado08/EternaPrimaveraa.git
cd EternaPrimaveraa
```
## Crear y activar el entorno virtual
 - Windows (PowerShell)
```bash
python -m venv env # Para crear
.\env\Scripts\activate # Para activar
```

 - Windows (cmd)
```bash
python -m venv env # Para crear
env\Scripts\activate.bat # Para activar
```

 - Linux / Mac
```bash
python3 -m venv env # Para crear
source env/bin/activate # Para activar
```
---

## Instalar dependencias

Con el entorno virtual activado, instala los paquetes necesarios:
```bash
pip install -r requirements.txt

```
## Preparar base de datos (antes del seed)

Debes comenzar desde cero para evitar errores relacionados con IDs duplicados o migraciones no sincronizadas.
### 1. Eliminar la base de datos:
- Windows (PowerShell)
```bash
del db.sqlite3

```

 - Linux / Mac
```bash
rm db.sqlite3

```
---

## Migraciones y seed

1. Crear nuevas migraciones:
```bash
python manage.py makemigrations

```
---

2. Aplicar migraciones:
```bash
python manage.py migrate

```
---

3. Cargar datos desde seed.sql (asegúrate que este archivo no contenga inserciones en tablas internas de Django como django_migrations, auth_user, etc.):
   
- Windows (PowerShell)
```bash
Get-Content datos.sql | sqlite3 db.sqlite3

```

 - Linux / Mac
```bash
sqlite3 db.sqlite3 < datos.sql

```
---


