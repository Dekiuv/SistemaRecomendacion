import pandas as pd

def load_data():
    aisles = pd.read_csv("data/Aisles.csv")
    departments = pd.read_csv("data/departments.csv")
    products = pd.read_csv("data/products.csv")
    orders = pd.read_csv("data/orders_cleaned.csv")
    order_products_prior = pd.read_csv("data/order_products__prior.csv")
    order_products_train = pd.read_csv("data/order_products__train.csv")

    # Unimos productos con aisles y departments
    products_full = products.merge(aisles, on='aisle_id') \
                            .merge(departments, on='department_id')

    return {
        "aisles": aisles,
        "departments": departments,
        "products": products,
        "products_full": products_full,
        "orders": orders,
        "order_products_prior": order_products_prior,
        "order_products_train": order_products_train
    }
