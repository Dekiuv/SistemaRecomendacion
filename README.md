# 🛒 Sistema de Recomendación para Instacart

Este proyecto es un sistema completo de recomendación de productos para supermercados tipo Instacart, desarrollado en Python y desplegado con una interfaz web en HTML, CSS y JavaScript, conectada a un backend Flask.

## 🎯 Objetivo del proyecto

- Analizar el historial de compras de usuarios.
- Ofrecer recomendaciones de productos personalizadas.
- Mejorar la experiencia del cliente y potenciar las ventas.

## 📁 Estructura del proyecto

```plaintext
SistemaRecomendacion/
├── data_loader.py             # Carga de los CSV
├── Creadorcluster.csv         # Segmentación de usuarios por K-Means
├── Codo+grafico.csv           # Visualizar grafico codo y distribución de usuarios en clusters
├── entreno.py                 # Entrena un modelo SVD por cada cluster
├── ver_metricas_modelos.py    # Muestra las métricas (accuracy, precision, recall, F1) de cada modelo entrenado.
├── recomendador.py            # Recomendación para un usuario y cluster.
├── nlp.py                     # Permite buscar productos similares usando procesamiento de lenguaje natural (TF-IDF).
├── market_basket.py           # Reglas de asociación (Apriori)
├── app.py                     # Backend Flask principal
├── index.html                 # Interfaz HTML principal
├── styles.css                 # Estilos CSS
├── script.js                  # Lógica del frontend en JavaScript
│
├── Image/                     # Carpeta con imagenes de la página web
│   ├── MAPA.png
│   ├── github.png
│   └── supermercado.png
│
├── modelos_por_clusters/      # Carpeta con modelos enternados
│   ├── modelo_svd_cluster0.pkl
│   ├── modelo_svd_cluster1.pkl
│   ├── modelo_svd_cluster2.pkl
│   └── modelo_svd_cluster3.pkl
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
- Utilizamos **Surprise (SVD)** para generar recomendaciones personalizadas.
- Entrenamos un modelo por cada **cluster de usuarios**, para mejorar la precisión.
- Se basa en la variable `reordered` como puntuación binaria (0 = no recompra, 1 = sí).
- El sistema predice productos no comprados que podrían interesar al usuario basándose en usuarios similares dentro de su mismo perfil.

### ✅ 2. Reglas de Asociación (Apriori)
- Aplicamos **mlxtend (Apriori)** para extraer reglas frecuentes entre productos comprados juntos (market basket analysis).
- Calculamos métricas como **soporte**, **confianza** y **lift**.
- Generamos reglas de la forma:  
  _“Si compras A, probablemente compres B”_.
- Filtramos las reglas **por tipo de usuario (cluster)** para que las recomendaciones sean más coherentes con su perfil.

### ✅ 3. Segmentación de Usuarios (K-Means)
- Agrupamos a los usuarios usando **KMeans** en base a sus compras por `aisle_id` y `department_id`.
- Creamos **clusters con perfiles definidos** como:
  - 🧼 Hogar completo & básicos
  - 🌿 Saludable y fresco
  - 🍞 Familiar y variado
  - 🍷 Gourmet & bebidas
- Cada usuario recibe un cluster y sus recomendaciones se ajustan a este perfil.

### ✅ 4. Sistema Híbrido Inteligente
- Combinamos **SVD + Reglas de asociación** para generar recomendaciones más sólidas:
  - SVD recomienda productos **no comprados** pero **populares entre similares**.
  - Apriori propone **productos complementarios** a las compras anteriores del usuario.
- Las recomendaciones están **filtradas por tipo de usuario**, basadas en su comportamiento y preferencias.

### ✅ 5. Búsqueda Semántica (TF-IDF)
- Incluimos un motor **NLP** para que el usuario pueda buscar productos escribiendo una palabra clave.
- Usamos **TF-IDF + Cosine Similarity** para encontrar coincidencias en nombres de productos.
- Permite búsquedas flexibles y relevantes aunque no se escriba el nombre exacto.

---

## 🌐 Interfaz web

Desarrollada con:
- HTML5
- CSS3
- JavaScript
- Backend en Flask + CORS

### Funcionalidades:
- Recomendaciones por ID de usuario basadas en algoritmos de filtrado colaborativo (SVD)
- Recomendaciones por perfil de usuario, segmentado por clústeres de consumo (K-Means)
- Búsqueda semántica (NLP): permite buscar productos escribiendo palabras clave
- Interfaz web visual e intuitiva

---

## 📚 Librerias necesarias

- 🐍 Python (3.11.9)
- 🐼 Pandas (2.2.3) -> Manipulación y análisis de los datos CSV
- 🔣 Numpy	(1.24.4) -> Operaciones matemáticas y estructuras base
- 🧩 Scikit-learn (1.6.1)	-> KMeans para segmentación de usuarios por pasillos
- 🎁 Surprise (1.1.4) -> SVD para sistema de recomendación colaborativa
- 🏪 Mlxtend (0.23.4) ->	Apriori y reglas de mercado (market basket analysis)
- 🔒 Joblib (1.4.2) -> Guardar y cargar el modelo entrenado en un archivo .pkl
- 🔌 Flask (3.1.0) -> Crear la API para conectar el frontend con el sistema de recomendación
- 💻 Flask-cors (5.0.1) -> Permitir peticiones desde Live Server (CORS)

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
- Y la carpeta `/modelos_por_cluster` (con los modelos entrenados)

**no están incluidos en este repositorio** por superar el límite de 100 MB por archivo.

### 📦 ¿Cómo obtener los datos?

- Puedes descargar los CSV desde la página oficial del dataset en Kaggle:  
  👉 [Instacart Market Basket Dataset](https://www.kaggle.com/code/yasserh/instacart-online-grocery-recommendation/input)

- Una vez descargados, colócalos en la carpeta:  
  `SistemaRecomendacion/data`

### 📌 ¿Qué hacer si el modelo no está?

La carpeta `/modelos_por_cluster` no está disponible, ejecutar `entreno.py` para obtener los modelos.

---
