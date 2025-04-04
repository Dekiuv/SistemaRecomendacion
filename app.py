from src.load_data import load_all_data
from src.preprocess import build_user_aisle_matrix
from src.clustering import segment_users, describe_clusters
from src.recommender import recommend_top_products_for_cluster
from src.clustering import plot_elbow_method, plot_user_clusters_pca

def main():
    aisles, departments, order_products_prior, order_products_train, orders, products = load_all_data()
    user_aisle_matrix, order_details, products_full = build_user_aisle_matrix(
        order_products_prior, orders, products, aisles, departments
    )

    user_clusters, model = segment_users(user_aisle_matrix, k=4)
    summary = describe_clusters(user_aisle_matrix, user_clusters)

    print("Resumen por cluster:")
    print(summary.head())

    cluster_id = 0
    print(f"\nTop productos recomendados para cluster {cluster_id}:")
    top_products = recommend_top_products_for_cluster(cluster_id, user_clusters, order_details, products_full)
    print(top_products)

    cluster_id = 1
    print(f"\nTop productos recomendados para cluster {cluster_id}:")
    top_products = recommend_top_products_for_cluster(cluster_id, user_clusters, order_details, products_full)
    print(top_products)

    cluster_id = 2
    print(f"\nTop productos recomendados para cluster {cluster_id}:")
    top_products = recommend_top_products_for_cluster(cluster_id, user_clusters, order_details, products_full)
    print(top_products)

    cluster_id = 3
    print(f"\nTop productos recomendados para cluster {cluster_id}:")
    top_products = recommend_top_products_for_cluster(cluster_id, user_clusters, order_details, products_full)
    print(top_products)

    # 1. Ver gráfico del codo
    plot_elbow_method(user_aisle_matrix)

    # 2. Entrenar KMeans con k=4 (una vez elegido)
    user_clusters, model = segment_users(user_aisle_matrix, k=5)

    # 3. Visualizar clusters en 2D
    plot_user_clusters_pca(user_aisle_matrix, user_clusters)
   

if __name__ == "__main__":
    main()