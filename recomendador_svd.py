import os
import joblib
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from data_loader import load_data

MODEL_PATH = "model\modelo_svd_binario.pkl"

def entrenar_svd_binario(order_products_prior, orders, model_path=MODEL_PATH):
    print("🔁 Entrenando modelo SVD con ratings binarios...")

    # Fusionar user_id y product_id
    df = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')

    # Crear columna binaria (comprado = 1)
    df['rating'] = 1

    # Eliminar duplicados user-product
    data = df[['user_id', 'product_id', 'rating']].drop_duplicates()

    # Preparar dataset para Surprise
    reader = Reader(rating_scale=(0, 1))
    dataset = Dataset.load_from_df(data[['user_id', 'product_id', 'rating']], reader)

    # Split
    trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

    # Entrenamiento
    model = SVD()
    model.fit(trainset)

    # Evaluación
    predictions = model.test(testset)
    rmse = accuracy.rmse(predictions)
    mae = accuracy.mae(predictions)

    # Guardar modelo
    joblib.dump(model, model_path)
    print(f"✅ Modelo guardado como '{model_path}'")

    return model, rmse, mae

def cargar_o_entrenar_modelo():
    if os.path.exists(MODEL_PATH):
        print("📁 Modelo ya guardado. Cargando desde disco...")
        model = joblib.load(MODEL_PATH)
        return model, None, None
    else:
        print("⚠️ No se encontró el modelo. Entrenando uno nuevo...")
        data = load_data()
        return entrenar_svd_binario(
            order_products_prior=data["order_products_prior"],
            orders=data["orders"]
        )
    
def recomendar_productos(model, user_id, products, order_products_prior, n=5):
    # Asegúrate de que el DataFrame tiene la columna user_id
    if 'user_id' not in order_products_prior.columns:
        raise ValueError("❌ Falta la columna 'user_id' en order_products_prior.")

    # Productos ya comprados por el usuario
    productos_comprados = order_products_prior[
        order_products_prior['user_id'] == user_id
    ]['product_id'].unique()

    # Filtrar productos NO comprados
    productos_no_comprados = products[~products['product_id'].isin(productos_comprados)]

    # Predecir probabilidad de recompra para cada producto
    predicciones = []
    for pid in productos_no_comprados['product_id']:
        est = model.predict(user_id, pid).est
        predicciones.append((pid, est))

    # Ordenar por score descendente
    predicciones.sort(key=lambda x: x[1], reverse=True)

    # Seleccionar los top-N productos
    top_ids = [pid for pid, _ in predicciones[:n]]

    # Devolver como DataFrame con nombres
    resultados = products[products['product_id'].isin(top_ids)][['product_id', 'product_name']].copy()
    resultados['score'] = resultados['product_id'].map(dict(predicciones))

    return resultados.sort_values(by='score', ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    modelo, rmse, mae = cargar_o_entrenar_modelo()

    if rmse and mae:
        print(f"\n📊 Evaluación del modelo:")
        print(f"RMSE: {rmse:.4f}")
        print(f"MAE:  {mae:.4f}")