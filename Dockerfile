FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala compiladores necesarios
RUN apt-get update && \
    apt-get install -y build-essential gcc g++ python3-dev && \
    apt-get clean

WORKDIR /app
COPY . .

# 🔽 Instala numpy primero antes del resto
RUN pip install --upgrade pip setuptools wheel
RUN pip install numpy==1.21.6

# Ahora sí instala todo el resto
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]