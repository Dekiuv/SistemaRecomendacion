# Importación de bibliotecas necesarias
from flask import Flask, request, jsonify        # Flask para crear la API web
from flask_cors import CORS                      # Para permitir solicitudes desde diferentes dominios (CORS)
from recomendador import recomendar_por_cluster_combinado  # Función para recomendar productos según cluster
from nlp import buscar_producto_o_departamento             # Función para búsqueda con NLP

# Creación de la aplicación Flask
app = Flask(__name__)

# Habilita CORS para que la API pueda ser consumida desde cualquier origen (frontend separado)
CORS(app)

# Ruta principal para verificar que la API está funcionando correctamente
@app.route("/")
def home():
    return "✅ API de Recomendación funcionando"

# Ruta para obtener recomendaciones mediante el método de clustering combinado y SVD
@app.route("/recomendar_svd")
def recomendar_svd():
    # Obtiene el parámetro "user_id" de la petición HTTP (como query parameter)
    user_id = int(request.args.get("user_id"))

    # Llama a la función que devuelve el cluster y recomendaciones para el usuario dado
    cluster_id, cluster_name, df = recomendar_por_cluster_combinado(user_id)

    # Verifica si el usuario existe y tiene recomendaciones
    if df is None:
        return jsonify({"error": "Usuario no encontrado o sin datos"})

    # Devuelve la respuesta en formato JSON con el usuario, su cluster y las recomendaciones
    return jsonify({
        "user_id": user_id,
        "cluster_id": cluster_id,
        "cluster_name": cluster_name,
        "recomendaciones": df.to_dict(orient="records")
    })

# Ruta para buscar productos o departamentos usando técnicas de NLP (búsqueda semántica)
@app.route("/buscar_producto")
def buscar_producto():
    # Obtiene el texto de búsqueda desde los parámetros de la petición HTTP
    query = request.args.get("query", "")

    # Realiza la búsqueda mediante la función NLP
    resultados = buscar_producto_o_departamento(query)

    # Devuelve los resultados en formato JSON
    return jsonify(resultados)

# Ejecuta la aplicación Flask en modo debug si el archivo se ejecuta directamente
if __name__ == "__main__":
    app.run(debug=True)