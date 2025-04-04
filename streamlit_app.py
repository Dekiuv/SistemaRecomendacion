import streamlit as st
from src.load_data import load_all_data
from src.preprocess import build_user_aisle_matrix
from src.clustering import segment_users
from src.recommender import recommend_top_products_for_cluster
from src.search_engine import ProductSearchEngine
from src.svd_recommender import SVDRecommenderLoaded
from src.market_basket import prepare_transactions, get_association_rules

st.title("🛒 Recomendador de productos - Instacart")

tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Buscar productos",
    "📦 Recomendaciones por cluster",
    "🎯 Recomendaciones personalizadas (SVD)",
    "🧺 Reglas de asociación (Market Basket)"
])

# Cargar y procesar datos
@st.cache_data
def prepare_data():
    aisles, departments, order_products_prior, order_products_train, orders, products = load_all_data()
    user_aisle_matrix, order_details, products_full = build_user_aisle_matrix(
        order_products_prior, orders, products, aisles, departments
    )
    user_clusters, _ = segment_users(user_aisle_matrix, k=4)
    return user_aisle_matrix, order_details, products_full, user_clusters

user_aisle_matrix, order_details, products_full, user_clusters = prepare_data()


with tab1:
    user_ids = user_clusters['user_id'].tolist()
    user_input = st.number_input("Introduce tu ID de usuario:", min_value=min(user_ids), max_value=max(user_ids), value=user_ids[0])

    # Obtener cluster y recomendaciones
    if user_input in user_ids:
        cluster_id = user_clusters[user_clusters['user_id'] == user_input]['cluster'].values[0]
        st.subheader(f"🧠 Usuario asignado al cluster {cluster_id}")
        st.write("Basado en tus compras, recomendamos:")

        recommended = recommend_top_products_for_cluster(cluster_id, user_clusters, order_details, products_full)
        st.table(recommended)
    else:
        st.warning("ID de usuario no encontrado.")

with tab2:
    st.subheader("🔎 Búsqueda de productos (NLP)")

    search_query = st.text_input("Escribe el nombre de un producto (ej: leche, avena, etc.)")

    if search_query:
        search_engine = ProductSearchEngine(products_full)
        results = search_engine.search(search_query, top_n=10)
        st.write("Resultados encontrados:")
        st.table(results)

with tab3:
    st.subheader("🎯 Recomendaciones personalizadas usando SVD (preentrenado)")
    user_input_svd = st.number_input("Introduce tu ID de usuario:", min_value=min(user_ids), max_value=max(user_ids), value=user_ids[0], key="svd_input")

    if user_input_svd in user_ids:
        svd_model = SVDRecommenderLoaded()
        svd_recommendations = svd_model.recommend_for_user(user_input_svd, products_full)

        st.write("Te recomendamos:")
        st.table(svd_recommendations)

with tab4:
    st.subheader("🧺 Productos que se compran juntos")

    min_support = st.slider("Soporte mínimo:", 0.001, 0.05, 0.01, step=0.001)
    min_conf = st.slider("Confianza mínima:", 0.1, 1.0, 0.2, step=0.05)

    basket = prepare_transactions(order_details, products_full)
    rules = get_association_rules(basket, min_support, min_conf)

    if not rules.empty:
        st.write("Reglas encontradas:")
        st.dataframe(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))
    else:
        st.warning("No se encontraron reglas con los parámetros seleccionados.")