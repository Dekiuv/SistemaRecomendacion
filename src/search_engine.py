import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProductSearchEngine:
    def __init__(self, products_df):
        self.products_df = products_df.copy()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.vectorizer.fit_transform(self.products_df['product_name'])

    def search(self, query, top_n=10):
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        top_indices = similarities.argsort()[::-1][:top_n]
        return self.products_df.iloc[top_indices][['product_id', 'product_name']]
