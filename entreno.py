import os
import pandas as pd
import joblib
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from data_loader import load_data

def entrenar_modelo_para_cluster(cluster_id, users_cluster, order_products_prior, orders, output_path):
    print(f"\n🔁 Entrenando modelo para cluster {cluster_id}...")

    # Filtrar datos por usuarios de este cluster
    df = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')
    df = df[df["user_id"].isin(users_cluster)]

    # Crear rating binario
    data = df.groupby(['user_id', 'product_id'])['reordered'].sum().reset_index()
    data['reordered'] = data['reordered'].apply(lambda x: 1 if x > 0 else 0)

    # Dataset para Surprise
    reader = Reader(rating_scale=(0, 1))
    dataset = Dataset.load_from_df(data[['user_id', 'product_id', 'reordered']], reader)
    trainset, testset = train_test_split(dataset, test_size=0.2, random_state=42)

    # Entrenamiento
    model = SVD()
    model.fit(trainset)
    predictions = model.test(testset)

    # Métricas
    rmse = accuracy.rmse(predictions, verbose=False)
    mae = accuracy.mae(predictions, verbose=False)

    y_true = [int(p.r_ui) for p in predictions]
    y_pred = [1 if p.est > 0.5 else 0 for p in predictions]
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='binary', zero_division=0)
    rec = recall_score(y_true, y_pred, average='binary', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='binary', zero_division=0)

    # Guardar
    model_info = {
        'model': model,
        'rmse': rmse,
        'mae': mae,
        'accuracy': acc,
        'precision': prec,
        'recall': rec,
        'f1': f1
    }

    filename = f"{output_path}/modelo_svd_cluster{cluster_id}.pkl"
    joblib.dump(model_info, filename)
    print(f"✅ Modelo del cluster {cluster_id} guardado en '{filename}'")

    return model_info

# 📦 Ejecutar todo
if __name__ == "__main__":
    output_path = "modelos_por_cluster"
    os.makedirs(output_path, exist_ok=True)

    data = load_data()
    order_products_prior = data["order_products_prior"]
    orders = data["orders"]

    user_segments = pd.read_csv("data\user_segments_combinado.csv")

    # Entrenar por cluster
    resultados = {}
    for cluster_id in sorted(user_segments["cluster"].unique()):
        users_cluster = user_segments[user_segments["cluster"] == cluster_id]["user_id"].tolist()
        resultados[cluster_id] = entrenar_modelo_para_cluster(
            cluster_id, users_cluster, order_products_prior, orders, output_path
        )

    print("\n📊 Entrenamiento finalizado para todos los clusters.")
