// Cliente del inventario: consume la API REST con Fetch.
const API = "/api/productos";
const STOCK_BAJO = 10;

const form = document.getElementById("form-producto");
const tabla = document.getElementById("tabla-productos");
const buscar = document.getElementById("buscar");
const btnGuardar = document.getElementById("btn-guardar");
const btnCancelar = document.getElementById("btn-cancelar");
const tituloForm = document.getElementById("titulo-form");
const aviso = document.getElementById("aviso");
const resumen = document.getElementById("resumen");
const campos = ["nombre", "descripcion", "precio", "cantidad_stock"];

let productos = [];
let temporizadorAviso;

const cop = new Intl.NumberFormat("es-CO", { style: "currency", currency: "COP", maximumFractionDigits: 0 });

function mostrarAviso(texto, esError = false) {
  aviso.textContent = texto;
  aviso.className = "aviso" + (esError ? " mal" : "");
  aviso.hidden = false;
  clearTimeout(temporizadorAviso);
  temporizadorAviso = setTimeout(() => (aviso.hidden = true), 3500);
}

function escapar(texto) {
  const d = document.createElement("div");
  d.textContent = texto ?? "";
  return d.innerHTML;
}

async function pedir(url, opciones = {}) {
  const resp = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...opciones,
  });
  const datos = await resp.json().catch(() => ({}));
  if (!resp.ok) throw { estado: resp.status, ...datos };
  return datos;
}

// ---------- Listado ----------
async function cargar() {
  try {
    const q = buscar.value.trim();
    productos = await pedir(q ? `${API}?q=${encodeURIComponent(q)}` : API);
    dibujar();
  } catch (e) {
    mostrarAviso(e.error || "No se pudo conectar con el servidor.", true);
  }
}

function dibujar() {
  const bajos = productos.filter((p) => p.cantidad_stock <= STOCK_BAJO).length;
  resumen.textContent = `${productos.length} productos, ${bajos} con stock bajo`;

  if (!productos.length) {
    tabla.innerHTML = `<tr><td colspan="6" class="vacio">No hay productos. Registra el primero en el formulario.</td></tr>`;
    return;
  }
  tabla.innerHTML = productos.map((p) => `
    <tr class="${p.cantidad_stock <= STOCK_BAJO ? "stock-bajo" : ""}">
      <td>${p.id_producto}</td>
      <td><strong>${escapar(p.nombre)}</strong><small>${escapar(p.descripcion)}</small></td>
      <td class="num">${cop.format(p.precio)}</td>
      <td class="num stock">${p.cantidad_stock}</td>
      <td>${escapar(p.fecha_registro)}</td>
      <td class="acc">
        <button class="secundario chico" data-editar="${p.id_producto}">Editar</button>
        <button class="peligro chico" data-eliminar="${p.id_producto}">Eliminar</button>
      </td>
    </tr>`).join("");
}

// ---------- Formulario ----------
function limpiarErrores() {
  document.querySelectorAll(".error").forEach((el) => (el.textContent = ""));
  campos.forEach((c) => form[c].classList.remove("invalido"));
}

function mostrarErrores(errores) {
  Object.entries(errores).forEach(([campo, msg]) => {
    const el = document.querySelector(`.error[data-for="${campo}"]`);
    if (el) el.textContent = msg;
    form[campo]?.classList.add("invalido");
  });
}

function validarLocal() {
  const e = {};
  if (!form.nombre.value.trim()) e.nombre = "El nombre es obligatorio.";
  const precio = Number(form.precio.value);
  if (form.precio.value === "" || isNaN(precio) || precio < 0) e.precio = "Ingresa un precio mayor o igual a 0.";
  const stock = Number(form.cantidad_stock.value);
  if (form.cantidad_stock.value === "" || !Number.isInteger(stock) || stock < 0) e.cantidad_stock = "Ingresa un entero mayor o igual a 0.";
  return e;
}

function modoEdicion(p) {
  document.getElementById("id_producto").value = p.id_producto;
  campos.forEach((c) => (form[c].value = p[c] ?? ""));
  tituloForm.textContent = `Editar producto #${p.id_producto}`;
  btnGuardar.textContent = "Guardar cambios";
  btnCancelar.hidden = false;
  form.nombre.focus();
}

function modoRegistro() {
  form.reset();
  document.getElementById("id_producto").value = "";
  tituloForm.textContent = "Nuevo producto";
  btnGuardar.textContent = "Registrar producto";
  btnCancelar.hidden = true;
  limpiarErrores();
}

form.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  limpiarErrores();
  const errores = validarLocal();
  if (Object.keys(errores).length) return mostrarErrores(errores);

  const id = document.getElementById("id_producto").value;
  const cuerpo = JSON.stringify({
    nombre: form.nombre.value,
    descripcion: form.descripcion.value,
    precio: form.precio.value,
    cantidad_stock: form.cantidad_stock.value,
  });
  try {
    await pedir(id ? `${API}/${id}` : API, { method: id ? "PUT" : "POST", body: cuerpo });
    mostrarAviso(id ? "Cambios guardados." : "Producto registrado.");
    modoRegistro();
    cargar();
  } catch (e) {
    if (e.campos) mostrarErrores(e.campos);
    mostrarAviso(e.error || "No se pudo guardar el producto.", true);
  }
});

btnCancelar.addEventListener("click", modoRegistro);

// ---------- Acciones de la tabla ----------
tabla.addEventListener("click", async (ev) => {
  const idEditar = ev.target.dataset.editar;
  const idEliminar = ev.target.dataset.eliminar;
  if (idEditar) {
    modoEdicion(productos.find((p) => p.id_producto == idEditar));
  } else if (idEliminar) {
    const p = productos.find((x) => x.id_producto == idEliminar);
    if (!confirm(`¿Eliminar "${p.nombre}"? Esta acción no se puede deshacer.`)) return;
    try {
      await pedir(`${API}/${idEliminar}`, { method: "DELETE" });
      mostrarAviso("Producto eliminado.");
      if (document.getElementById("id_producto").value == idEliminar) modoRegistro();
      cargar();
    } catch (e) {
      mostrarAviso(e.error || "No se pudo eliminar el producto.", true);
    }
  }
});

let esperaBusqueda;
buscar.addEventListener("input", () => {
  clearTimeout(esperaBusqueda);
  esperaBusqueda = setTimeout(cargar, 250);
});

cargar();
