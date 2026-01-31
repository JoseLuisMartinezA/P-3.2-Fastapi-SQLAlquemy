# API REST de Inventario - FastAPI + SQLAlchemy

## Temática
Este proyecto implementa una API REST para la gestión de un catálogo de productos y categorías. Permite realizar operaciones CRUD completas sobre ambos recursos, manteniendo la persistencia en una base de datos SQLite.

## Entidades
El sistema gestiona dos entidades principales:

1. **Category (Categorías)**: Representa los grupos de productos.
   - `id`: Identificador único (autogenerado).
   - `name`: Nombre de la categoría (único).
   - `description`: Descripción opcional.
   - `is_active`: Estado de la categoría.
   - `created_at`: Fecha de creación automática.

2. **Product (Productos)**: Representa los artículos individuales.
   - `id`: Identificador único (autogenerado).
   - `name`: Nombre del producto.
   - `description`: Descripción opcional.
   - `price`: Precio del producto (validad mayor que 0).
   - `stock`: Cantidad disponible (validado mayor o igual a 0).
   - `category_id`: Clave foránea que relaciona el producto con una categoría.

## Requisitos
- Python 3.8+
- FastAPI
- SQLAlchemy
- Uvicorn
- Pydantic

## Instalación y Ejecución

1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   ```

2. Activa el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Ejecuta la aplicación:
   ```bash
   cd app
   fastapi dev main.py
   ```
   O usando uvicorn:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

## Documentación
Una vez iniciada la aplicación, la documentación interactiva está disponible en:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Organización del Proyecto
La estructura sigue las mejores prácticas de modularización:
- `app/main.py`: Punto de entrada y configuración de CORS.
- `app/database/`: Configuración de SQLAlchemy y sesión.
- `app/models/`: Modelos de la base de datos (ORM).
- `app/schemas/`: Esquemas de Pydantic para validación y respuesta.
- `app/routes/`: Definición de los endpoints de la API.
