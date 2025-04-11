import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# ✅ Función: análisis de cesta de mercado
def market_basket_analysis(order_products_prior, products, min_support=0.005, metric='lift',
                           min_threshold=1, max_orders=10000):
    print(f"🔄 Procesando los primeros {max_orders:,} pedidos para análisis de cesta...")

    pedidos_filtrados = order_products_prior[order_products_prior['order_id'] <= max_orders]
    pedidos = pedidos_filtrados.merge(products[['product_id', 'product_name']], on='product_id')

    transacciones = pedidos.groupby('order_id')['product_name'].apply(list).tolist()

    te = TransactionEncoder()
    trans_bin = te.fit_transform(transacciones)
    df_trans = pd.DataFrame(trans_bin, columns=te.columns_)

    print("✅ Datos listos. Generando itemsets frecuentes...")
    itemsets = apriori(df_trans, min_support=min_support, use_colnames=True)

    reglas = association_rules(itemsets, metric=metric, min_threshold=min_threshold)
    print(f"🔍 Reglas generadas: {len(reglas)}")

    return reglas.sort_values(by='lift', ascending=False)

# ✅ Función: recomendaciones por reglas para un usuario
def recomendaciones_por_reglas_usuario(user_id, order_products_prior, orders, products, reglas,
                                       min_confidence=0.2, min_lift=2.0):
    if 'user_id' not in order_products_prior.columns:
        order_products_prior = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')

    productos_usuario = order_products_prior[order_products_prior['user_id'] == user_id]
    productos_usuario = productos_usuario.merge(products[['product_id', 'product_name']], on='product_id')
    productos_usuario = productos_usuario['product_name'].unique()

    reglas_usuario = reglas[reglas['antecedents'].apply(
        lambda ant: any(prod in ant for prod in productos_usuario)
    )]

    reglas_usuario = reglas_usuario[reglas_usuario['consequents'].apply(
        lambda cons: all(p not in productos_usuario for p in cons)
    )]

    if 'confidence' not in reglas_usuario.columns or 'lift' not in reglas_usuario.columns:
        return pd.DataFrame()

    reglas_usuario = reglas_usuario[
        (reglas_usuario['confidence'] >= min_confidence) &
        (reglas_usuario['lift'] >= min_lift)
    ]

    if reglas_usuario.empty:
        return pd.DataFrame()

    return reglas_usuario[['antecedents', 'consequents', 'support', 'confidence', 'lift']] \
        .sort_values(by='lift', ascending=False).reset_index(drop=True)