import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from data_loader import load_data

# Segmentación por pasillos
def segmentar_por_aisles(order_products_prior, orders, products, aisles, n_clusters=4):
    merged = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')
    merged = merged.merge(products[['product_id', 'aisle_id']], on='product_id')
    merged = merged.merge(aisles, on='aisle_id')

    user_aisle = merged.groupby(['user_id', 'aisle'])['product_id'].count().unstack(fill_value=0)

    scaler = StandardScaler()
    user_aisle_scaled = scaler.fit_transform(user_aisle)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    user_aisle['cluster'] = kmeans.fit_predict(user_aisle_scaled)

    return user_aisle.reset_index()[['user_id', 'cluster']]

# Visualización PCA
def visualizar_clusters_por_aisles(order_products_prior, orders, products, aisles, n_clusters=4):
    merged = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')
    merged = merged.merge(products[['product_id', 'aisle_id']], on='product_id')
    merged = merged.merge(aisles, on='aisle_id')

    user_aisle = merged.groupby(['user_id', 'aisle'])['product_id'].count().unstack(fill_value=0)

    scaler = StandardScaler()
    user_aisle_scaled = scaler.fit_transform(user_aisle)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(user_aisle_scaled)

    pca = PCA(n_components=2)
    componentes = pca.fit_transform(user_aisle_scaled)

    df_pca = pd.DataFrame(componentes, columns=["PC1", "PC2"])
    df_pca["cluster"] = clusters

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_pca, x="PC1", y="PC2", hue="cluster", palette="Set2", s=60)
    plt.title("Segmentación de Usuarios por Pasillos (KMeans + PCA)")
    plt.xlabel("Componente Principal 1")
    plt.ylabel("Componente Principal 2")
    plt.legend(title="Cluster")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    return df_pca

# Método del Codo
def metodo_del_codo(order_products_prior, orders, products, aisles, max_k=10):
    merged = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')
    merged = merged.merge(products[['product_id', 'aisle_id']], on='product_id')
    merged = merged.merge(aisles, on='aisle_id')

    user_aisle = merged.groupby(['user_id', 'aisle'])['product_id'].count().unstack(fill_value=0)

    scaler = StandardScaler()
    user_aisle_scaled = scaler.fit_transform(user_aisle)

    inercia = []
    for k in range(1, max_k + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(user_aisle_scaled)
        inercia.append(kmeans.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_k + 1), inercia, marker='o')
    plt.xlabel('Número de Clusters (k)')
    plt.ylabel('Inercia')
    plt.title('Método del Codo - Clustering por Pasillos')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("elbow.png")  # Guarda el gráfico
    plt.show()


# Ejecución directa
if __name__ == "__main__":
    data = load_data()

    print("Mostrando gráfico del método del codo...")
    metodo_del_codo(
        data["order_products_prior"],
        data["orders"],
        data["products"],
        data["aisles"],
        max_k=10
    )

    print("\nSegmentando usuarios con KMeans (k=4)...")
    segmentados = segmentar_por_aisles(
        data["order_products_prior"],
        data["orders"],
        data["products"],
        data["aisles"],
        n_clusters=4
    )
    print(segmentados.head())

    print("\nMostrando visualización de los clusters...")
    visualizar_clusters_por_aisles(
        data["order_products_prior"],
        data["orders"],
        data["products"],
        data["aisles"],
        n_clusters=4
    )