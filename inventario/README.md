# Sistema Web de Gestión de Inventario

CRUD de productos: HTML5/CSS3/JavaScript (frontend), Python + Flask (backend), MySQL (base de datos).

## Requisitos
- Python 3.14 (funciona también con 3.10+)
- MySQL 8

## Puesta en marcha
1. Crear la base de datos y la tabla:
   ```
   mysql -u root -p < database/schema.sql
   ```
2. Instalar dependencias:
   ```
   cd backend
   python -m venv venv
   venv\Scripts\activate        # Linux/Mac: source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configurar la conexión (variables de entorno; por defecto root sin contraseña):
   ```
   set DB_USER=root
   set DB_PASSWORD=tu_clave      # Linux/Mac: export DB_PASSWORD=tu_clave
   ```
4. Ejecutar:
   ```
   python app.py
   ```
5. Abrir http://localhost:5000

## API REST
| Método | Ruta                    | Acción                       |
|--------|-------------------------|------------------------------|
| GET    | /api/productos          | Listar (opcional `?q=texto`) |
| GET    | /api/productos/<id>     | Consultar uno                |
| POST   | /api/productos          | Crear                        |
| PUT    | /api/productos/<id>     | Actualizar                   |
| DELETE | /api/productos/<id>     | Eliminar                     |

Cuerpo JSON: `{"nombre": "...", "descripcion": "...", "precio": 1000, "cantidad_stock": 5}`

## Estructura
- `database/schema.sql`: DDL y datos de ejemplo
- `backend/`: `app.py` (rutas), `models.py` (clase Producto y validaciones), `database.py` (repositorio MySQL)
- `frontend/`: interfaz web (se sirve desde Flask)
