def build_user_aisle_matrix(order_products_prior, orders, products, aisles, departments):
    products_full = products.merge(aisles, on='aisle_id', how='left') \
                            .merge(departments, on='department_id', how='left')

    orders_prior = orders[orders['eval_set'] == 'prior']
    order_details = order_products_prior.merge(orders_prior[['order_id', 'user_id']], on='order_id', how='left')
    order_details = order_details.merge(products_full[['product_id', 'aisle']], on='product_id', how='left')

    user_aisle = order_details.groupby(['user_id', 'aisle'])['product_id'].count().reset_index()
    user_aisle.rename(columns={'product_id': 'product_count'}, inplace=True)

    user_aisle_matrix = user_aisle.pivot_table(index='user_id', columns='aisle', values='product_count', fill_value=0)

    return user_aisle_matrix, order_details, products_full