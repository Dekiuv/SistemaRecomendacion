from flask import Flask, request, jsonify
from flask_cors import CORS

from data_loader import load_data
from market_basket import market_basket_analysis, recomendaciones_por_reglas_usuario
from recomendador_svd import entrenar_svd_binario, recomendar_productos
import joblib

app = Flask(__name__)
CORS(app)  # Permite que JS acceda desde otra URL

# Cargar datos y reglas
data = load_data()
order_products_prior = data["order_products_prior"]
orders = data["orders"]
products = data["products"]

# Asegurarse de tener user_id
if 'user_id' not in order_products_prior.columns:
    order_products_prior = order_products_prior.merge(orders[['order_id', 'user_id']], on='order_id')

# Generar reglas al iniciar
reglas = market_basket_analysis(order_products_prior, products)

# Cargar modelo SVD
try:
    model_svd = joblib.load("modelo_svd_binario.pkl")
except:
    model_svd, _, _ = entrenar_svd_binario(order_products_prior, orders)
    joblib.dump(model_svd, "modelo_svd_binario.pkl")

# Endpoint de recomendación híbrida
@app.route('/recomendar')
def recomendar():
    user_id = int(request.args.get("user_id"))
    recomendaciones_svd = recomendar_productos(model_svd, user_id, products, order_products_prior, n=5)
    recomendaciones_reglas = recomendaciones_por_reglas_usuario(
        user_id, order_products_prior, orders, products, reglas
    )

    nombres_svd = list(recomendaciones_svd['product_name'])
    nombres_reglas = set()
    if not recomendaciones_reglas.empty:
        for cons in recomendaciones_reglas['consequents']:
            for prod in cons:
                if prod not in nombres_svd:
                    nombres_reglas.add(prod)

    return jsonify({
        "svd": nombres_svd,
        "reglas": list(nombres_reglas)
    })

# Endpoint de buscador (modo demo)
@app.route('/buscar')
def buscar():
    query = request.args.get("query", "").lower()
    resultados = products[products['product_name'].str.lower().str.contains(query)]
    return jsonify(resultados['product_name'].head(10).tolist())

if __name__ == '__main__':
    app.run(debug=True)
