import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# 📥 Cargar los datos
aisles = pd.read_csv("data/Aisles.csv")
departments = pd.read_csv("data/departments.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders_cleaned.csv")
order_products_prior = pd.read_csv("data/order_products__prior.csv")

# 🔗 Unir datos de productos con aisles y departments
products_full = products.merge(aisles, on="aisle_id").merge(departments, on="department_id")

# 🔁 Unir pedidos con usuarios y productos
df = order_products_prior.merge(orders[["order_id", "user_id"]], on="order_id")
df = df.merge(products_full[["product_id", "aisle", "department"]], on="product_id")

# 📊 Crear tabla usuario × pasillo (aisle)
pivot_aisle = df.pivot_table(index="user_id", columns="aisle", values="product_id", aggfunc="count").fillna(0)

# 📊 Crear tabla usuario × departamento
pivot_dept = df.pivot_table(index="user_id", columns="department", values="product_id", aggfunc="count").fillna(0)

# 🔀 Combinar ambas tablas
pivot_combined = pd.concat([pivot_aisle, pivot_dept], axis=1)

# 🔧 Normalizar
scaler = StandardScaler()
pivot_scaled = pd.DataFrame(
    scaler.fit_transform(pivot_combined),
    index=pivot_combined.index,
    columns=pivot_combined.columns
)

# 🎯 Aplicar KMeans con 4 clusters
kmeans = KMeans(n_clusters=4, random_state=42)
pivot_scaled["cluster"] = kmeans.fit_predict(pivot_scaled)

# 🧠 Ver las 5 características más relevantes por cluster
cluster_summary = pivot_scaled.groupby("cluster").mean()

print("\n📊 Top 5 características por cluster (mezcla de pasillos y departamentos):\n")
for i in range(cluster_summary.shape[0]):
    top_features = cluster_summary.iloc[i].sort_values(ascending=False).head(5).index.tolist()
    print(f"🧠 Cluster {i}: {', '.join(top_features)}")

# 💾 Guardar segmentos
pivot_scaled.reset_index()[["user_id", "cluster"]].to_csv("data/user_segments_combinado.csv", index=False)
print("\n✅ Segmentación combinada completada y guardada como 'user_segments_combinado.csv'")
