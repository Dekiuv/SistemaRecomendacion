# Imagen de Python 3.9 compatible con scikit-surprise
FROM python:3.9-slim

# Variables para evitar archivos bytecode y tener logs visibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias necesarias para compilación
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ python3-dev && \
    apt-get clean

# Crea el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools wheel

# Instala las dependencias del proyecto
RUN pip install -r requirements.txt

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la app Flask
CMD ["python", "app.py"]