import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def prepare_transactions(order_details, products_full, max_orders=5000):
    # Unir productos con nombres
    merged = order_details.merge(products_full[['product_id', 'product_name']], on='product_id', how='left')

    # Filtrar para evitar explosión de memoria
    sample_orders = merged['order_id'].drop_duplicates().sample(n=max_orders, random_state=42)
    filtered = merged[merged['order_id'].isin(sample_orders)]

    # Crear matriz binaria: cada fila = una orden, cada columna = un producto
    basket = filtered.groupby(['order_id', 'product_name'])['product_id'] \
                     .count().unstack().fillna(0).astype(int)

    # Convertir a 1/0 para Apriori
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)

    return basket

def get_association_rules(basket, min_support=0.01, min_confidence=0.2):
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=min_confidence)
    return rules.sort_values('lift', ascending=False)