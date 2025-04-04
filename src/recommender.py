def recommend_top_products_for_cluster(cluster_id, user_clusters, order_details, products_full, top_n=10):
    users_in_cluster = user_clusters[user_clusters['cluster'] == cluster_id]['user_id']
    cluster_orders = order_details[order_details['user_id'].isin(users_in_cluster)]

    top_products = cluster_orders['product_id'].value_counts().head(top_n).index.tolist()
    product_names = products_full[products_full['product_id'].isin(top_products)][['product_id', 'product_name']]

    return product_names.drop_duplicates().reset_index(drop=True)