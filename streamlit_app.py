# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# ------------------ CARGAR DATOS ------------------

st.set_page_config(page_title="Recomendador Instacart", layout="centered")

@st.cache_data
def cargar_datos():
    user_product_matrix = pd.read_pickle("user_product_matrix.pkl")
    preds_df = pd.read_pickle("preds_df.pkl")
    products = pd.read_csv("Dataset\products.csv")
    return user_product_matrix, preds_df, products

user_product_matrix, preds_df, products = cargar_datos()

st.title("🛒 Sistema de Recomendación - Instacart")

# ------------------ BÚSQUEDA TF-IDF ------------------

st.header("🔍 Buscar productos")

@st.cache_data
def construir_tfidf():
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(products["product_name"])
    return vectorizer, tfidf_matrix

vectorizer, tfidf_matrix = construir_tfidf()

query = st.text_input("Escribe una palabra clave:")
if query:
    query_vec = vectorizer.transform([query])
    sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_n = sim.argsort()[-10:][::-1]
    resultados = products.iloc[top_n][["product_name"]]
    st.write("🔎 Resultados más similares:")
    st.dataframe(resultados)

# ------------------ RECOMENDACIÓN SVD ------------------

st.header("🎯 Recomendaciones SVD")

user_id_input = st.number_input("Introduce tu ID de usuario:", min_value=0, step=1)

def recomendar_svd(user_id, n=5):
    if user_id not in preds_df.index:
        return pd.DataFrame({"Mensaje": ["❌ Usuario no encontrado."]})
    user_row = preds_df.loc[user_id].sort_values(ascending=False)
    productos_comprados = user_product_matrix.loc[user_id]
    no_comprados = user_row[productos_comprados == 0]
    top_ids = no_comprados.head(n).index
    return products[products["product_id"].isin(top_ids)][["product_name"]]

if st.button("Recomendar productos"):
    recomendaciones = recomendar_svd(user_id_input)
    st.write("🛍 Productos recomendados:")
    st.dataframe(recomendaciones)