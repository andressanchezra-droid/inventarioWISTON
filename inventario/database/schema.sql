-- Sistema Web de Gestión de Inventario - Script DDL/DML
CREATE DATABASE IF NOT EXISTS inventario_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE inventario_db;

CREATE TABLE IF NOT EXISTS productos (
  id_producto    INT AUTO_INCREMENT PRIMARY KEY,
  nombre         VARCHAR(100)  NOT NULL,
  descripcion    TEXT          NULL,
  precio         DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
  cantidad_stock INT           NOT NULL DEFAULT 0 CHECK (cantidad_stock >= 0),
  fecha_registro TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE INDEX idx_productos_nombre ON productos (nombre);

INSERT INTO productos (nombre, descripcion, precio, cantidad_stock) VALUES
 ('Teclado mecánico', 'Teclado USB, switches rojos', 185000.00, 25),
 ('Mouse inalámbrico', 'Sensor óptico 1600 DPI', 65000.00, 40),
 ('Monitor 24"', 'Panel IPS Full HD', 620000.00, 8);
