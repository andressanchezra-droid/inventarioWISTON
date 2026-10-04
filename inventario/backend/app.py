"""API REST del Sistema Web de Gestión de Inventario (Flask)."""
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from mysql.connector import Error as MySQLError

from database import ProductoRepository
from models import Producto, ValidationError

FRONTEND = Path(__file__).resolve().parent.parent / "frontend"
app = Flask(__name__, static_folder=str(FRONTEND), static_url_path="")
repo = ProductoRepository()


def serializar(fila):
    """Convierte Decimal y datetime a tipos compatibles con JSON."""
    return {
        **fila,
        "precio": float(fila["precio"]),
        "fecha_registro": fila["fecha_registro"].strftime("%Y-%m-%d %H:%M"),
    }


@app.get("/")
def inicio():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/api/productos")
def listar():
    busqueda = request.args.get("q", "").strip()
    return jsonify([serializar(f) for f in repo.listar(busqueda)])


@app.get("/api/productos/<int:id_producto>")
def obtener(id_producto):
    fila = repo.obtener(id_producto)
    if not fila:
        return jsonify({"error": "Producto no encontrado."}), 404
    return jsonify(serializar(fila))


@app.post("/api/productos")
def crear():
    producto = Producto.desde_json(request.get_json(silent=True))
    nuevo_id = repo.crear(producto)
    return jsonify(serializar(repo.obtener(nuevo_id))), 201


@app.put("/api/productos/<int:id_producto>")
def actualizar(id_producto):
    producto = Producto.desde_json(request.get_json(silent=True))
    if not repo.actualizar(id_producto, producto):
        return jsonify({"error": "Producto no encontrado."}), 404
    return jsonify(serializar(repo.obtener(id_producto)))


@app.delete("/api/productos/<int:id_producto>")
def eliminar(id_producto):
    if not repo.eliminar(id_producto):
        return jsonify({"error": "Producto no encontrado."}), 404
    return jsonify({"mensaje": "Producto eliminado."})


@app.errorhandler(ValidationError)
def error_validacion(e):
    return jsonify({"error": "Datos inválidos.", "campos": e.errores}), 400


@app.errorhandler(MySQLError)
def error_bd(e):
    app.logger.error("Error de base de datos: %s", e)
    return jsonify({"error": "No se pudo completar la operación en la base de datos."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
