from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import seaborn as sns
import pandas as pd

def segment_users(user_aisle_matrix, k=5):
    scaler = StandardScaler()
    user_aisle_scaled = scaler.fit_transform(user_aisle_matrix)

    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(user_aisle_scaled)

    user_clusters = pd.DataFrame({'user_id': user_aisle_matrix.index, 'cluster': clusters})

    return user_clusters, kmeans

def describe_clusters(user_aisle_matrix, user_clusters):
    user_aisle_with_cluster = user_aisle_matrix.copy()
    user_aisle_with_cluster['cluster'] = user_clusters['cluster'].values
    cluster_summary = user_aisle_with_cluster.groupby('cluster').mean()
    return cluster_summary

def plot_elbow_method(user_aisle_matrix, max_k=10):
    inertias = []
    for k in range(1, max_k + 1):
        model = KMeans(n_clusters=k, random_state=42)
        model.fit(user_aisle_matrix)
        inertias.append(model.inertia_)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, max_k + 1), inertias, 'o--')
    plt.title('Método del Codo')
    plt.xlabel('Número de Clusters (K)')
    plt.ylabel('Inercia')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_user_clusters_pca(user_aisle_matrix, user_clusters):
    # Reducir dimensiones con PCA
    pca = PCA(n_components=2)
    components = pca.fit_transform(user_aisle_matrix)

    # Crear DataFrame para plotear
    df_plot = pd.DataFrame(components, columns=['x', 'y'])
    df_plot['cluster'] = user_clusters['cluster'].values

    # Plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_plot, x='x', y='y', hue='cluster', palette='viridis', s=70)
    plt.title("Visualización de clusters de usuarios (PCA sobre pasillos)")
    plt.xlabel("Patrón de compra por pasillos")
    plt.ylabel("Comportamiento diferencial entre segmentos")
    plt.legend(title="Segmento")
    plt.tight_layout()
    plt.show()
