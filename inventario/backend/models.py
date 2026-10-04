"""Modelo Producto (POO) con validaciones de negocio."""
from decimal import Decimal, InvalidOperation


class ValidationError(Exception):
    def __init__(self, errores):
        super().__init__("Datos inválidos")
        self.errores = errores


class Producto:
    def __init__(self, nombre, descripcion, precio, cantidad_stock):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad_stock = cantidad_stock

    @classmethod
    def desde_json(cls, datos):
        """Valida y construye un Producto; lanza ValidationError si hay fallas."""
        datos = datos or {}
        errores = {}

        nombre = str(datos.get("nombre", "")).strip()
        if not nombre:
            errores["nombre"] = "El nombre es obligatorio."
        elif len(nombre) > 100:
            errores["nombre"] = "El nombre no puede superar 100 caracteres."

        descripcion = str(datos.get("descripcion") or "").strip()

        try:
            precio = Decimal(str(datos.get("precio")))
            if not precio.is_finite() or precio < 0 or precio > Decimal("99999999.99"):
                raise ValueError
            precio = precio.quantize(Decimal("0.01"))
        except (InvalidOperation, ValueError, TypeError):
            errores["precio"] = "El precio debe ser un número mayor o igual a 0."
            precio = None

        try:
            stock = int(str(datos.get("cantidad_stock")))
            if stock < 0:
                raise ValueError
        except (ValueError, TypeError):
            errores["cantidad_stock"] = "El stock debe ser un entero mayor o igual a 0."
            stock = None

        if errores:
            raise ValidationError(errores)
        return cls(nombre, descripcion, precio, stock)
