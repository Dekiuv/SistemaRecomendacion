const API_URL = "http://127.0.0.1:5000";

// 🔍 Buscador NLP
function buscar() {
  const query = document.getElementById("searchInput").value;
  if (!query) return alert("Escribe algo para buscar.");

  fetch(`${API_URL}/buscar?query=${query}`)
    .then(res => res.json())
    .then(data => {
      let html = "<ul>";
      data.forEach(prod => {
        html += `<li>${prod}</li>`;
      });
      html += "</ul>";
      document.getElementById("resultadosBusqueda").innerHTML = html;
    })
    .catch(err => {
      document.getElementById("resultadosBusqueda").innerText = "❌ Error al buscar.";
      console.error(err);
    });
}

// 🧠 Recomendaciones híbridas
function recomendar() {
  const userId = document.getElementById("userIdInput").value;
  if (!userId) return alert("Introduce un user_id válido.");

  document.getElementById("recomendaciones").innerHTML = "🔄 Generando recomendaciones...";

  fetch(`${API_URL}/recomendar?user_id=${userId}`)
    .then(res => res.json())
    .then(data => {
      let html = "<h3>🔹 Recomendación basada en lo que han comprado otras personas (SVD):</h3><ul>";
      data.svd.forEach(prod => html += `<li>${prod}</li>`);
      html += "</ul><h3>🔸 Recomendación basada únicamente en lo que has comprado (Market):</h3><ul>";
      data.reglas.forEach(prod => html += `<li>${prod}</li>`);
      html += "</ul>";
      document.getElementById("recomendaciones").innerHTML = html;
    })
    .catch(err => {
      document.getElementById("recomendaciones").innerText = "❌ Error al obtener recomendaciones.";
      console.error(err);
    });
}
