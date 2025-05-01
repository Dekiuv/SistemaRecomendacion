from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from recomendador import recomendar_por_cluster_combinado
from nlp import buscar_producto_o_departamento

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route("/")
def home():
    return send_file("index.html")

@app.route('/Image/<path:filename>')
def image_files(filename):
    return send_from_directory('Image', filename)

from flask import send_from_directory

# CSS
@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

# JS
@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')


@app.route("/recomendar_svd")
def recomendar_svd():
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
    query = request.args.get("query", "")
    resultados = buscar_producto_o_departamento(query)
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(debug=False)