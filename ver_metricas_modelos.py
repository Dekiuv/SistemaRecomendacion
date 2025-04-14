import joblib
import os

# Ruta donde se guardaron los modelos
carpeta_modelos = "modelos_por_cluster"

# Mostrar métricas de cada modelo
for i in range(4):
    ruta = os.path.join(carpeta_modelos, f"modelo_svd_cluster{i}.pkl")

    if os.path.exists(ruta):
        datos = joblib.load(ruta)

        print(f"\n📦 Modelo del Cluster {i}")
        print(f"RMSE:      {datos['rmse']:.4f}")
        print(f"MAE:       {datos['mae']:.4f}")
        print(f"Accuracy:  {datos['accuracy']:.4f}")
        print(f"Precision: {datos['precision']:.4f}")
        print(f"Recall:    {datos['recall']:.4f}")
        print(f"F1-Score:  {datos['f1']:.4f}")
    else:
        print(f"\n❌ No se encontró el modelo del cluster {i}")
