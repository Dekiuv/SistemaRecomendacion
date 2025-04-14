import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 📥 Cargar datos
aisles = pd.read_csv("data/Aisles.csv")
departments = pd.read_csv("data/departments.csv")
products = pd.read_csv("data/products.csv")
orders = pd.read_csv("data/orders_cleaned.csv")
order_products_prior = pd.read_csv("data/order_products__prior.csv")

# 🔗 Unir productos con info
products_full = products.merge(aisles, on="aisle_id").merge(departments, on="department_id")
df = order_products_prior.merge(orders[["order_id", "user_id"]], on="order_id")
df = df.merge(products_full[["product_id", "aisle", "department"]], on="product_id")

# 📊 Pivot de pasillos + departamentos
pivot_aisle = df.pivot_table(index="user_id", columns="aisle", values="product_id", aggfunc="count").fillna(0)
pivot_dept = df.pivot_table(index="user_id", columns="department", values="product_id", aggfunc="count").fillna(0)
pivot_combined = pd.concat([pivot_aisle, pivot_dept], axis=1)

# ⚖️ Normalizar
scaler = StandardScaler()
pivot_scaled = pd.DataFrame(
    scaler.fit_transform(pivot_combined),
    index=pivot_combined.index,
    columns=pivot_combined.columns
)

# 📉 Gráfico del Codo
inertias = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(pivot_scaled)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K_range, inertias, marker='o')
plt.title("Método del Codo para elegir número de clusters")
plt.xlabel("Número de Clusters (K)")
plt.ylabel("Inercia")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🎯 KMeans final con 4 clusters
kmeans_final = KMeans(n_clusters=4, random_state=42)
pivot_scaled["cluster"] = kmeans_final.fit_predict(pivot_scaled)

# 🔄 PCA para reducción a 2D
pca = PCA(n_components=2)
pca_result = pca.fit_transform(pivot_scaled.drop(columns=["cluster"]))
pca_df = pd.DataFrame(pca_result, columns=["PC1", "PC2"])
pca_df["cluster"] = pivot_scaled["cluster"].values

# 🎨 Visualización de Clusters en 2D
plt.figure(figsize=(8, 6))
for c in sorted(pca_df["cluster"].unique()):
    subset = pca_df[pca_df["cluster"] == c]
    plt.scatter(subset["PC1"], subset["PC2"], label=f"Cluster {c}", alpha=0.6)

plt.title("Visualización de usuarios segmentados por clusters (PCA)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
