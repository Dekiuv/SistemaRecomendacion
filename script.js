const API_URL = "http://127.0.0.1:5000";

function buscar() {
  const input = document.getElementById("busqueda").value.trim().toLowerCase();
  document.getElementById("textoBusqueda").textContent = input;
  const tabla = document.getElementById("tablaResultados");
  const modal = document.getElementById("modalCarga");
  tabla.innerHTML = "";

  if (!input) {
    alert("Introduce un producto o un id de usuario.");
    return;
  }

  modal.style.display = "flex"; // Mostrar carga

  if (input.startsWith("id")) {
    const user_id = parseInt(input.replace("id", ""));
    if (isNaN(user_id)) {
      modal.style.display = "none";
      alert("Formato inválido. Usa id + número. Ej: id27");
      return;
    }

    fetch(`${API_URL}/recomendar_svd?user_id=${user_id}`)
      .then(res => res.json())
      .then(data => {
        modal.style.display = "none"; // Ocultar carga
        if (data.error) {
          tabla.innerHTML = `<tr><td colspan="3">❌ ${data.error}</td></tr>`;
        } else {
          data.recomendaciones.forEach(prod => {
            tabla.innerHTML += `
              <tr>
                <td>${prod.product_name}</td>
                <td>${prod.department}</td>
                <td>${prod.aisle}</td>
              </tr>
            `;
          });
        }
      })
      .catch(() => {
        modal.style.display = "none";
        tabla.innerHTML = `<tr><td colspan="3">❌ Error al obtener recomendaciones.</td></tr>`;
      });

  } else {
    fetch(`${API_URL}/buscar_producto?query=${encodeURIComponent(input)}`)
      .then(res => res.json())
      .then(data => {
        modal.style.display = "none"; // Ocultar carga
        if (!data.length) {
          tabla.innerHTML = `<tr><td colspan="3">❌ No se encontraron productos.</td></tr>`;
        } else {
          data.forEach(prod => {
            tabla.innerHTML += `
              <tr>
                <td>${prod.product_name}</td>
                <td>${prod.department}</td>
                <td>${prod.aisle}</td>
              </tr>
            `;
          });
        }
      })
      .catch(() => {
        modal.style.display = "none";
        tabla.innerHTML = `<tr><td colspan="3">❌ Error al buscar producto.</td></tr>`;
      });
  }
}