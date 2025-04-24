import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 📥 Cargar datos
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders_cleaned.csv")
order_products = pd.read_csv("data/order_products__prior.csv")
user_segments = pd.read_csv("data/user_segments_combinado.csv")

# 🔢 Pedir cluster
cluster_id = int(input("🔢 Introduce el número de cluster (0-3): "))

# 🎯 Definir departamentos dominantes por cluster
departamentos_cluster = {
    0: ["household", "cleaning products", "personal care", "oral hygiene"],
    1: ["produce", "dairy eggs"],
    2: ["snacks", "pantry", "bakery", "dry goods pasta"],
    3: ["beverages", "alcohol", "frozen"]
}

# 🎯 Filtrar usuarios del cluster
usuarios_cluster = user_segments[user_segments["cluster"] == cluster_id]["user_id"].unique()

# 🔄 Obtener pedidos de esos usuarios
orders_cluster = orders[orders["user_id"].isin(usuarios_cluster)]
order_ids_cluster = orders_cluster["order_id"].unique()

# 🔗 Filtrar pedidos + productos
df = order_products[order_products["order_id"].isin(order_ids_cluster)]
df = df.merge(products[["product_id", "product_name", "department_id"]], on="product_id")

# 🔗 Unir con departamentos para filtrar correctamente
departments = pd.read_csv("data/departments.csv")
df = df.merge(departments, on="department_id")

# 🔹 Filtrar productos frecuentes
producto_frecuente = df['product_name'].value_counts()
productos_validos = producto_frecuente[producto_frecuente > 800].index
df = df[df['product_name'].isin(productos_validos)]

# 🎯 Filtrar solo productos de los departamentos del cluster
departamentos_validos = departamentos_cluster.get(cluster_id, [])
df = df[df['department'].isin(departamentos_validos)]

# 🧺 Agrupar pedidos
transacciones = df.groupby("order_id")["product_name"].apply(list).tolist()

# 🔧 Codificar para Apriori
te = TransactionEncoder()
trans_bin = te.fit_transform(transacciones)
df_bin = pd.DataFrame(trans_bin, columns=te.columns_)

# 📊 Apriori (⚡ bajamos min_support a 0.005)
itemsets = apriori(df_bin, min_support=0.006, use_colnames=True)
reglas = association_rules(itemsets, metric="lift", min_threshold=1.2)

# 🧽 Limpiar y ordenar
reglas = reglas.sort_values("lift", ascending=False)
top_reglas = reglas[["antecedents", "consequents", "support", "confidence", "lift"]].head(10)

# 📤 Guardar como CSV
output_file = f"reglas_cluster_{cluster_id}_dep.csv"
top_reglas.to_csv(output_file, index=False)

# 📋 Mostrar
print(f"\n📊 Top 10 reglas de asociación para el cluster {cluster_id} (filtrado por departamentos):\n")
print(top_reglas.to_string(index=False))
print(f"\n✅ Reglas guardadas en: {output_file}")
