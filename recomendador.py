import pandas as pd

# Diccionario de nombres por cluster
nombres_cluster_combinado = {
    0: "🧼 Hogar completo & básicos",
    1: "🌿 Saludable y fresco",
    2: "🍞 Familiar y variado",
    3: "🍷 Gourmet & bebidas"
}

# Departamentos clave por cluster
departamentos_por_cluster = {
    0: ["household", "cleaning products", "personal care", "oral hygiene"],
    1: ["produce", "dairy eggs"],
    2: ["snacks", "pantry", "dry goods pasta", "bakery"],
    3: ["alcohol", "beverages", "frozen", "packaged produce"]
}

def recomendar_por_cluster_combinado(user_id, top_n=5):
    orders = pd.read_csv("data/orders_cleaned.csv", usecols=["order_id", "user_id"])
    order_products_prior = pd.read_csv("data/order_products__prior.csv", usecols=["order_id", "product_id"])
    products = pd.read_csv("data/products.csv", usecols=["product_id", "product_name", "aisle_id", "department_id"])
    departments = pd.read_csv("data/departments.csv")
    aisles = pd.read_csv("data/aisles.csv")
    user_segments = pd.read_csv("data/user_segments_combinado.csv")

    if user_id not in user_segments["user_id"].values:
        return None, None, None

    cluster_id = int(user_segments[user_segments["user_id"] == user_id]["cluster"].values[0])
    cluster_name = nombres_cluster_combinado.get(cluster_id, "Desconocido")

    products_full = products.merge(aisles, on="aisle_id").merge(departments, on="department_id")

    usuarios_cluster = user_segments[user_segments["cluster"] == cluster_id]["user_id"].values

    # 🔥 Filtrar las órdenes antes del merge
    orders_cluster = orders[orders["user_id"].isin(usuarios_cluster)]
    df = order_products_prior.merge(orders_cluster, on="order_id")

    products_cluster = df.merge(products_full, on="product_id")
    filtrados = products_cluster[products_cluster["department"].isin(departamentos_por_cluster[cluster_id])]

    productos_populares = filtrados["product_id"].value_counts().index.tolist()
    productos_usuario = df[df["user_id"] == user_id]["product_id"].unique()
    recomendaciones = [pid for pid in productos_populares if pid not in productos_usuario][:top_n]

    resultado = products_full[products_full["product_id"].isin(recomendaciones)][
        ["product_id", "product_name", "aisle", "department"]
    ].reset_index(drop=True)

    return cluster_id, cluster_name, resultado