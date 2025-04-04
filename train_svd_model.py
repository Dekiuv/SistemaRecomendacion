import pandas as pd
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import accuracy
import pickle

from src.load_data import load_all_data
from src.preprocess import build_user_aisle_matrix

# 1. Cargar datos
aisles, departments, order_products_prior, order_products_train, orders, products = load_all_data()
_, order_details, _ = build_user_aisle_matrix(order_products_prior, orders, products, aisles, departments)

# 2. Crear dataset user-product-rating
data = order_details.groupby(['user_id', 'product_id']).size().reset_index(name='rating')
reader = Reader(rating_scale=(1, data['rating'].max()))
dataset = Dataset.load_from_df(data[['user_id', 'product_id', 'rating']], reader)

# 3. Dividir en entrenamiento y prueba
trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

# 4. Entrenar el modelo
model = SVD()
model.fit(trainset)

# 5. Evaluar el modelo
predictions = model.test(testset)
rmse = accuracy.rmse(predictions)
mae = accuracy.mae(predictions)

print(f"\n✅ Evaluación del modelo:")
print(f"🔹 RMSE: {rmse:.4f}")
print(f"🔹 MAE: {mae:.4f}")

# 6. Guardar el modelo
with open('models/svd_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# 7. Guardar los datos de entrenamiento
data.to_csv('models/svd_data.csv', index=False)

print("\n✅ Modelo SVD entrenado y guardado con éxito.")
