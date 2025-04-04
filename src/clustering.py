from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import pandas as pd

def segment_users(user_aisle_matrix, k=4):
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