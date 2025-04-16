import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 🔹 Entrada de cluster
cluster_id = int(input("🔢 Introduce el número de cluster (0-3): "))

# 📦 Cargar datos
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders_cleaned.csv")
order_products = pd.read_csv("data/order_products__prior.csv")
user_segments = pd.read_csv("data/user_segments_combinado.csv")

# 🔍 Filtrar usuarios del cluster
usuarios_cluster = user_segments[user_segments["cluster"] == cluster_id]["user_id"].unique()

# 🔄 Unir con orders para obtener order_id
orders_cluster = orders[orders["user_id"].isin(usuarios_cluster)]
order_ids_cluster = orders_cluster["order_id"].unique()

# 🔄 Filtrar pedidos del cluster
df = order_products[order_products["order_id"].isin(order_ids_cluster)]
df = df.merge(products[["product_id", "product_name"]], on="product_id")

# 🔁 Agrupar por order_id
transacciones = df.groupby("order_id")["product_name"].apply(list).tolist()

# 🔧 Codificar
te = TransactionEncoder()
trans_bin = te.fit_transform(transacciones)
df_bin = pd.DataFrame(trans_bin, columns=te.columns_)

# 📊 Apriori y reglas
itemsets = apriori(df_bin, min_support=0.01, use_colnames=True)
reglas = association_rules(itemsets, metric="lift", min_threshold=1.2)
reglas = reglas.sort_values("lift", ascending=False)

# 🧾 Mostrar resultados
print(f"\n📊 Top 10 reglas del cluster {cluster_id}:\n")
print(reglas[["antecedents", "consequents", "support", "confidence", "lift"]].head(10).to_string(index=False))