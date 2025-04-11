import pandas as pd
import joblib
from data_loader import load_data
from market_basket import market_basket_analysis
from market_basket import market_basket_analysis, recomendaciones_por_reglas_usuario
from recomendador_svd import entrenar_svd_binario, recomendar_productos

# ✅ Script híbrido
if __name__ == "__main__":
    print("📦 Cargando datos...")
    data = load_data()
    orders = data["orders"]
    order_products_prior = data["order_products_prior"]
    products = data["products"]

    # Añadir user_id a order_products_prior si no lo tiene
    if 'user_id' not in order_products_prior.columns:
        order_products_prior = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')

    # 📌 User ID
    user_id = int(input("🧑 Introduce el user_id: "))

    # ✅ Recomendaciones por SVD
    try:
        print("🔍 Cargando modelo SVD...")
        model_svd = joblib.load("model\modelo_svd_binario.pkl")
    except:
        print("⚠️ Modelo no encontrado. Entrenando...")
        model_svd, _, _ = entrenar_svd_binario(order_products_prior, orders)
        joblib.dump(model_svd, "model\modelo_svd_binario.pkl")

    print("🔮 Obteniendo recomendaciones por SVD...")
    recomendaciones_svd = recomendar_productos(model_svd, user_id, products, order_products_prior, n=5)

    # ✅ Reglas de asociación
    print("📊 Generando reglas de mercado...")
    reglas = market_basket_analysis(order_products_prior, products, max_orders=10000, min_support=0.005)

    print("🧠 Buscando recomendaciones por reglas...")
    recomendaciones_reglas = recomendaciones_por_reglas_usuario(
        user_id,
        order_products_prior,
        orders,
        products,
        reglas,
        min_confidence=0.2,
        min_lift=2.0
    )

    # ✅ Combinar resultados
    nombres_svd = set(recomendaciones_svd['product_name'])
    nombres_reglas = set()

    if not recomendaciones_reglas.empty:
        for consec in recomendaciones_reglas['consequents']:
            for prod in consec:
                nombres_reglas.add(prod)

    print("\n📋 Recomendaciones híbridas para el usuario", user_id)
    print("🔹 Desde SVD:")
    for prod in nombres_svd:
        print("   ✅", prod)

    print("🔸 Desde reglas de mercado:")
    for prod in nombres_reglas:
        if prod not in nombres_svd:
            print("   🧠", prod)
