import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Carga y unión de productos con departamentos y pasillos
def cargar_datos():
    products = pd.read_csv("data/products.csv")
    departments = pd.read_csv("data/departments.csv")
    aisles = pd.read_csv("data/Aisles.csv")

    products = products.merge(departments, on="department_id")
    products = products.merge(aisles, on="aisle_id")

    return products, departments

# 🔍 Función principal de búsqueda
def buscar_producto_o_departamento(palabra_clave, top_n=10):
    palabra_clave = palabra_clave.lower()
    products, departments = cargar_datos()

    # Si coincide con un departamento exacto
    departamentos = departments['department'].str.lower()
    if palabra_clave in departamentos.values:
        department_id = departments[departments['department'].str.lower() == palabra_clave]['department_id'].values[0]
        productos_en_departamento = products[products['department_id'] == department_id]
        return productos_en_departamento[['product_name', 'department', 'aisle']].drop_duplicates().sort_values("product_name").to_dict(orient="records")

    # Si es búsqueda por nombre de producto
    nombres = products['product_name'].fillna('').str.lower()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(nombres)
    consulta_vector = tfidf.transform([palabra_clave])
    similitudes = cosine_similarity(consulta_vector, tfidf_matrix).flatten()
    indices = similitudes.argsort()[-top_n:][::-1]

    resultados = products.iloc[indices][['product_name', 'department', 'aisle']].copy()
    resultados['score'] = similitudes[indices]

    return resultados.drop_duplicates().to_dict(orient="records")