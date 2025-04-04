import pandas as pd

def load_all_data(data_path='Dataset/'):
    aisles = pd.read_csv(f'{data_path}aisles.csv')
    departments = pd.read_csv(f'{data_path}departments.csv')
    order_products_prior = pd.read_csv(f'{data_path}order_products__prior.csv')
    order_products_train = pd.read_csv(f'{data_path}order_products__train.csv')
    orders = pd.read_csv(f'{data_path}orders_cleaned.csv')
    products = pd.read_csv(f'{data_path}products.csv')

    return aisles, departments, order_products_prior, order_products_train, orders, products

