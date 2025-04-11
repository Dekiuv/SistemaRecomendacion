from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def buscar_producto_o_departamento(palabra_clave, products, departments, top_n=5):
    palabra_clave = palabra_clave.lower()

    # Buscar por nombre de departamento
    departamentos = departments['department'].str.lower()
    if palabra_clave in departamentos.values:
        # Si coincide con un departamento, devolver todos los productos del mismo
        department_id = departments[departments['department'].str.lower() == palabra_clave]['department_id'].values[0]
        productos_en_departamento = products[products['department_id'] == department_id]
        return productos_en_departamento[['product_id', 'product_name']].sort_values('product_name')

    # Si no es departamento, usar búsqueda por TF-IDF
    nombres = products['product_name'].fillna('').str.lower()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(nombres)
    consulta_vector = tfidf.transform([palabra_clave])
    sim = cosine_similarity(consulta_vector, tfidf_matrix).flatten()
    indices = sim.argsort()[-top_n:][::-1]
    resultados = products.iloc[indices][['product_id', 'product_name']]
    resultados['score'] = sim[indices]
    return resultados.reset_index(drop=True)