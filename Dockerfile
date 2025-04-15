# Usa imagen de Python 3.11 con Debian como base
FROM python:3.11-slim

# Evita generación de .pyc y asegura log en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala compiladores necesarios para scikit-surprise y otros
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ python3-dev && \
    apt-get clean

# Crea carpeta de trabajo
WORKDIR /app

# Copia todos los archivos del proyecto
COPY . .

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools wheel

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Expone el puerto (Railway lo manejará dinámicamente)
EXPOSE 5000

# Comando para ejecutar la app Flask
CMD ["python", "app.py"]