import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# 📥 Cargar datos
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders_cleaned.csv")
order_products = pd.read_csv("data/order_products__prior.csv")

# 🔗 Unir pedidos con productos
df = order_products.merge(products[["product_id", "product_name"]], on="product_id")

# 🏆 Filtrar los 100 productos más populares
productos_populares = df['product_name'].value_counts().head(100).index
df = df[df['product_name'].isin(productos_populares)]

# 🔽 Filtrar a máximo 100,000 pedidos (para que pese menos)
pedidos_muestreados = df['order_id'].drop_duplicates().sample(n=100000, random_state=42)
df = df[df['order_id'].isin(pedidos_muestreados)]

# 🛒 Agrupar productos por pedido
transacciones = df.groupby('order_id')['product_name'].apply(list).tolist()

# 🔧 Codificar para Apriori
te = TransactionEncoder()
trans_bin = te.fit_transform(transacciones)
df_bin = pd.DataFrame(trans_bin, columns=te.columns_)

# 📊 Aplicar Apriori
itemsets = apriori(df_bin, min_support=0.01, use_colnames=True)

# 🧠 Generar reglas de asociación
reglas = association_rules(itemsets, metric="lift", min_threshold=1.2)

# 📋 Mostrar top 10 reglas
top_reglas = reglas.sort_values("lift", ascending=False)[["antecedents", "consequents", "support", "confidence", "lift"]].head(10)

print("\n📊 Top 10 reglas de asociación basadas en los 100 productos más populares:\n")
print(top_reglas.to_string(index=False))

# 💾 Guardar en CSV
top_reglas.to_csv("mba_top100_productos.csv", index=False)
print("\n✅ Reglas guardadas en 'MBA.csv'")