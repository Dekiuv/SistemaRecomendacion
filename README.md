# 🛒 Sistema de Recomendación para Instacart

Este proyecto desarrolla un sistema de recomendación personalizado para usuarios de Instacart, una plataforma de compras online de supermercado. El sistema permite segmentar usuarios, buscar productos, recomendar artículos personalizados y sugerir productos complementarios usando datos históricos de compras.

---

## 🎯 Objetivos del Proyecto

- 📊 **Segmentación de usuarios** según su comportamiento de compra por pasillo (K-Means)
- 🔍 **Motor de búsqueda inteligente** para encontrar productos por palabras clave (NLP)
- 🤖 **Sistema de recomendación personalizado** mediante filtrado colaborativo (SVD)
- 🧺 **Análisis de cesta de la compra** (Market Basket Analysis, próximamente)
- 🌐 **Interfaz web interactiva** con Streamlit

---

> ⚠️ Nota: Los archivos en `Dataset/` y `models/` han sido excluidos del repositorio por su tamaño. Puedes recrearlos ejecutando:
>
> - `train_svd_model.py` para entrenar y guardar el modelo SVD
> - Añadir tus propios CSV en la carpeta `Dataset/`
