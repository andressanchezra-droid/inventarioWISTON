"""Conexión a MySQL. La configuración se toma de variables de entorno."""
import os
import mysql.connector

CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "inventario_db"),
}


def get_connection():
    return mysql.connector.connect(**CONFIG)


class ProductoRepository:
    """Acceso a datos de la tabla productos (consultas parametrizadas)."""

    COLUMNAS = "id_producto, nombre, descripcion, precio, cantidad_stock, fecha_registro"

    def _ejecutar(self, sql, params=(), lectura=False, uno=False):
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(sql, params)
            if lectura:
                return cur.fetchone() if uno else cur.fetchall()
            conn.commit()
            return cur.lastrowid, cur.rowcount
        finally:
            conn.close()

    def listar(self, busqueda=""):
        sql = f"SELECT {self.COLUMNAS} FROM productos"
        params = ()
        if busqueda:
            sql += " WHERE nombre LIKE %s OR descripcion LIKE %s"
            params = (f"%{busqueda}%", f"%{busqueda}%")
        return self._ejecutar(sql + " ORDER BY id_producto DESC", params, lectura=True)

    def obtener(self, id_producto):
        return self._ejecutar(
            f"SELECT {self.COLUMNAS} FROM productos WHERE id_producto = %s",
            (id_producto,), lectura=True, uno=True)

    def crear(self, p):
        nuevo_id, _ = self._ejecutar(
            "INSERT INTO productos (nombre, descripcion, precio, cantidad_stock) "
            "VALUES (%s, %s, %s, %s)",
            (p.nombre, p.descripcion, p.precio, p.cantidad_stock))
        return nuevo_id

    def actualizar(self, id_producto, p):
        # rowcount puede ser 0 si no hubo cambios; se verifica existencia aparte
        self._ejecutar(
            "UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, "
            "cantidad_stock=%s WHERE id_producto=%s",
            (p.nombre, p.descripcion, p.precio, p.cantidad_stock, id_producto))
        return self.obtener(id_producto) is not None

    def eliminar(self, id_producto):
        _, filas = self._ejecutar(
            "DELETE FROM productos WHERE id_producto = %s", (id_producto,))
        return filas > 0
