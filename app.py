from src.load_data import load_all_data
from src.preprocess import build_user_aisle_matrix
from src.clustering import segment_users, describe_clusters
from src.recommender import recommend_top_products_for_cluster

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

if __name__ == "__main__":
    main()