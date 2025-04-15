from flask import Flask, request, jsonify
from flask_cors import CORS
from recomendador import recomendar_por_cluster_combinado
from nlp import buscar_producto_o_departamento

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ API de Recomendación funcionando"

@app.route("/recomendar_svd")
def recomendar_svd():
    from recomendador import recomendar_por_cluster_combinado  # o como se llame tu módulo
    user_id = int(request.args.get("user_id"))
    cluster_id, cluster_name, df = recomendar_por_cluster_combinado(user_id)
    if df is None:
        return jsonify({"error": "Usuario no encontrado o sin datos"})
    return jsonify({
        "user_id": user_id,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "recomendaciones": df.to_dict(orient="records")
    })

@app.route("/buscar_producto")
def buscar_producto():
    from nlp import buscar_producto_o_departamento
    query = request.args.get("query", "")
    resultados = buscar_producto_o_departamento(query)
    return jsonify(resultados)  # resultados ya es una lista de diccionarios

if __name__ == "__main__":
    app.run(debug=True)