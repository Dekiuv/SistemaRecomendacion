# 🛒 Sistema de Recomendación para Instacart

Este proyecto es un sistema completo de recomendación de productos para supermercados tipo Instacart, desarrollado en Python y desplegado con una interfaz web en HTML, CSS y JavaScript, conectada a un backend Flask.

## 🎯 Objetivo del proyecto

- Analizar el historial de compras de los usuarios.
- Ofrecer recomendaciones de productos personalizadas.
- Mejorar la experiencia del cliente y potenciar las ventas.

---

## 📁 Estructura del proyecto

```plaintext
SistemaRecomendacion/
├── app.py                     # Backend Flask principal
├── data_loader.py             # Carga de los CSV (función load_data)
├── recomendador_svd.py        # Entrenamiento y predicción con SVD
├── market_basket.py           # Reglas de asociación (Apriori) y recomendaciones por reglas
├── sistema_hibrido.py         # Motor de recomendación que combina SVD + Reglas
├── segmentos.csv              # Segmentación de usuarios por K-Means
├── modelo_svd_binario.pkl     # Modelo SVD entrenado (excluido de GitHub si es muy grande)
├── index.html                 # Interfaz HTML principal
├── styles.css                 # Estilos CSS
├── script.js                  # Lógica del frontend en JavaScript
│
├── data/                      # Carpeta con los CSV
│   ├── Aisles.csv
│   ├── departments.csv
│   ├── order_products__prior.csv
│   ├── order_products__train.csv
│   ├── orders_cleaned.csv
│   └── products.csv
│
├── .gitignore                 # Archivos y carpetas ignoradas por Git
└── README.md                  # Documentación del proyecto
```
---

## 📊 Algoritmos utilizados

### ✅ 1. Filtrado Colaborativo (SVD)
- Utiliza la librería `Surprise` para predecir productos que podrían interesar al usuario según lo que han comprado otros usuarios similares.
- Entrena un modelo SVD con la variable `reordered` como calificación implícita.

### ✅ 2. Reglas de Asociación (Apriori)
- Analiza millones de pedidos para encontrar combinaciones frecuentes de productos (market basket analysis).
- Usa `mlxtend` para extraer reglas tipo:  
  “Si compras A, probablemente compres B”.

### ✅ 3. Segmentación de Usuarios (K-Means)
- Agrupa usuarios según sus compras por pasillo (`aisle_id`) para descubrir patrones de comportamiento.
- Cada usuario recibe un segmento con una descripción clara.

### ✅ 4. Sistema Híbrido
- Combina las recomendaciones SVD + Reglas de mercado.
- SVD sugiere productos nuevos de otros usuarios similares.
- Las reglas proponen productos complementarios a tus compras.

---

## 🌐 Interfaz web

Desarrollada con:
- HTML5
- CSS3
- JavaScript
- Backend en Flask + CORS

### Funcionalidades:
- 🧠 Buscador por palabra clave (producto o categoría)
- 🧑 Input para introducir un `user_id`
- 📊 Resultados de recomendación híbrida
- 📍 Muestra el tipo de comprador (segmento)

---

## 📚 Librerias necesarias

- 🐍 Python (3.11.9)
- 🐼 Pandas () -> Manipulación y análisis de los datos CSV
- 🔣 Numpy	() -> Operaciones matemáticas y estructuras base
- 🧩 Scikit-learn ()	-> KMeans para segmentación de usuarios por pasillos
- 🎁 Surprise () -> SVD para sistema de recomendación colaborativa
- 🏪 Mlxtend () ->	Apriori y reglas de mercado (market basket analysis)
- 🔒 Joblib () -> Guardar y cargar el modelo entrenado en un archivo .pkl
- 🔌 Flask () -> Crear la API para conectar el frontend con el sistema de recomendación
- 💻 Flask-cors () -> Permitir peticiones desde Live Server (CORS)

---

## 🚀 ¿Cómo ejecutar el proyecto?

### 1. Instala los requerimientos

```bash
pip install flask flask-cors pandas surprise scikit-learn mlxtend

```
### 2. Ejecutar programa

```bash
python app.py
```
---

## ⚠️ Aviso

- La carpeta `/data` (con los archivos CSV)
- El archivo `modelo_svd_binario.pkl` (modelo SVD entrenado)

**no están incluidos en este repositorio** por superar el límite de 100 MB por archivo.

### 📦 ¿Cómo obtener los datos?

- Puedes descargar los CSV desde la página oficial del dataset en Kaggle:  
  👉 [Instacart Market Basket Dataset](https://www.kaggle.com/code/yasserh/instacart-online-grocery-recommendation/input)

- Una vez descargados, colócalos en la carpeta:  
  `SistemaRecomendacion/data`

### 📌 ¿Qué hacer si el modelo no está?

Si `modelo_svd_binario.pkl` no está disponible, el backend Flask **lo entrenará automáticamente** al iniciar `app.py`.

---
