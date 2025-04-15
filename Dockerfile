# Imagen oficial de Python optimizada
FROM python:3.11-slim

# Evita que Python guarde archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que el buffer de salida se vea en Railway
ENV PYTHONUNBUFFERED=1

# Crea directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Actualiza pip y setuptools
RUN pip install --upgrade pip setuptools wheel

# Instala las dependencias
RUN pip install -r requirements.txt

# Expone el puerto (Railway lo redefine, pero esto es bueno tenerlo)
EXPOSE 5000

# Comando para ejecutar la app
CMD ["python", "app.py"]