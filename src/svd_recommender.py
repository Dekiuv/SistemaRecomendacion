# src/svd_recommender.py

import pandas as pd
import pickle

class SVDRecommenderLoaded:
    def __init__(self, model_path='models/svd_model.pkl', data_path='models/svd_data.csv'):
        self.model = pickle.load(open(model_path, 'rb'))
        self.data = pd.read_csv(data_path)

    def recommend_for_user(self, user_id, products_full, n=10):
        all_products = products_full['product_id'].unique()
        purchased = set(self.data[self.data['user_id'] == user_id]['product_id'])

        predictions = []
        for pid in all_products:
            if pid not in purchased:
                pred = self.model.predict(user_id, pid)
                predictions.append((pid, pred.est))

        predictions.sort(key=lambda x: x[1], reverse=True)
        top_ids = [pid for pid, _ in predictions[:n]]
        return products_full[products_full['product_id'].isin(top_ids)][['product_id', 'product_name']].drop_duplicates()