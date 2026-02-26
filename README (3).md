# Práctica guiada – Contenerización y despliegue de una aplicación Python

## Contexto de la práctica

En la práctica 3.2 se desarrolló una aplicación backend en Python utilizando **FastAPI** y una base de datos **SQLite**.

En esta práctica se va a dar el paso hacia un entorno de despliegue real:

- La aplicación se ejecutará dentro de un contenedor Docker
- La base de datos SQLite será sustituida por **PostgreSQL**
- PostgreSQL se ejecutará en un contenedor independiente
- Ambos servicios se orquestarán mediante **Docker Compose**
- Finalmente, la aplicación se desplegará en un servicio online como **Render**

---

## Objetivos de la práctica

Al finalizar la práctica el alumnado será capaz de:

- Contenerizar una aplicación FastAPI
- Sustituir SQLite por PostgreSQL
- Configurar una conexión entre contenedores
- Usar volúmenes para persistencia de datos
- Orquestar servicios con Docker Compose
- Desplegar una aplicación backend en la nube

---

## Paso 1 – Preparación del proyecto

Partir del proyecto desarrollado en la **práctica 3.2**.

Estructura aproximada del proyecto:

```
.
├── main.py
├── database
├── models
├── routes
├── schemas
├── requirements.txt
```

Comprobar que:

- La aplicación funciona correctamente en local
- Los endpoints responden correctamente

---

## Paso 2 – Sustitución de SQLite por PostgreSQL

### 2.1 Modificar la configuración de la base de datos

Hasta ahora la aplicación utilizaba SQLite.

Se sustituirá la URL de conexión por una de PostgreSQL.

Ejemplo de URL de conexión:

```
postgresql://usuario:password@host:5432/nombre_bd
```

La URL se leerá desde una variable de entorno llamada `DATABASE_URL`.

---

### 2.2 Actualizar el código de conexión

En el archivo de configuración de la base de datos:

```
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
```

Esto permite que la aplicación:

- Funcione en local
- Funcione en Docker
- Funcione en producción

---

## Paso 3 – Crear el Dockerfile de la aplicación

Crear un archivo `Dockerfile` en la raíz del proyecto.

Ejemplo:

```
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Este archivo define cómo se construye la imagen de la aplicación.

---

## Paso 4 – Crear el docker-compose.yml

Se utilizará Docker Compose para orquestar:

- El contenedor de la API
- El contenedor de PostgreSQL
- El volumen de persistencia

---

### 4.1 Definición del servicio de PostgreSQL

El servicio de base de datos utilizará una imagen oficial.

Parámetros:

- Usuario
- Contraseña
- Nombre de base de datos
- Volumen de datos

---

### 4.2 Definición del servicio de la API

El servicio de la API:

- Se construye desde el Dockerfile
- Expone el puerto 8000
- Depende del servicio de base de datos
- Recibe la URL de conexión por variable de entorno

---

### 4.3 Archivo docker-compose.yml completo

```
services:
  api:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://app:app123@db:5432/appdb

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app123
      POSTGRES_DB: appdb
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Paso 5 – Creación automática de las tablas

Las tablas no las crea Docker ni PostgreSQL.

Las crea la aplicación a partir de los modelos.

En `main.py`:

```
from database.database import engine, Base
from models.user import User

Base.metadata.create_all(bind=engine)
```

---

## Paso 6 – Ejecución del proyecto con Docker Compose

Desde la raíz del proyecto ejecutar:

```
docker compose up -d
```

Comprobar:

- Que ambos contenedores están en ejecución
- Que la API responde en `http://localhost:8000`
- Que los datos se guardan correctamente

---

## Paso 7 – Comprobación de la persistencia de datos

1. Insertar datos mediante la API
2. Detener los contenedores:

```
docker compose down
```

3. Volver a levantarlos:

```
docker compose up -d
```

Resultado esperado:

- Los datos siguen existiendo gracias al volumen

---

## Paso 8 – Preparación para despliegue en Render

Antes de desplegar:

- Subir el proyecto a un repositorio GitHub
- Verificar que la aplicación usa variables de entorno
- Eliminar configuraciones dependientes de local

---

## Paso 9 – Despliegue en Render

### 9.1 Crear el servicio web

En Render:

- Crear un nuevo **Web Service**
- Conectar el repositorio
- Indicar que es una aplicación Docker

---

### 9.2 Crear la base de datos PostgreSQL

En Render:

- Crear un servicio **PostgreSQL**
- Obtener la URL de conexión

---

### 9.3 Configurar variables de entorno

En el servicio web:

- Definir la variable `DATABASE_URL`
- Usar la URL proporcionada por Render

---

## Paso 10 – Verificación final

Comprobar que:

- La aplicación responde online
- Los endpoints funcionan correctamente
- Los datos persisten entre despliegues

---

## Entrega de la práctica

El alumnado deberá entregar:

- Repositorio GitHub del proyecto
- Archivo `docker-compose.yml`
- Dockerfile
- URL pública de la aplicación desplegada

---

## Resultado final

Se ha transformado una aplicación local en una aplicación backend:

- Contenerizada
- Orquestada
- Persistente
- Desplegada en producción

## Rúbrica de evaluación – Práctica de contenerización y despliegue

La siguiente rúbrica se utilizará para evaluar la práctica de contenerización, orquestación y despliegue de la aplicación backend.

La puntuación total de la práctica es de **10 puntos**.

---

### 1. Contenerización de la aplicación (2 puntos)

| Criterio            | Descripción                                                                   | Puntuación |
| ------------------- | ----------------------------------------------------------------------------- | ---------- |
| Dockerfile correcto | Existe un Dockerfile funcional que construye y ejecuta la aplicación FastAPI  | 1          |
| Imagen funcional    | La imagen se construye correctamente y la aplicación arranca en el contenedor | 1          |

---

### 2. Sustitución de SQLite por PostgreSQL (2 puntos)

| Criterio                               | Descripción                                                       | Puntuación |
| -------------------------------------- | ----------------------------------------------------------------- | ---------- |
| Uso de PostgreSQL                      | La aplicación utiliza PostgreSQL en lugar de SQLite               | 1          |
| Configuración por variables de entorno | La conexión a la base de datos se realiza mediante `DATABASE_URL` | 1          |

---

### 3. Docker Compose y orquestación de servicios (2,5 puntos)

| Criterio                     | Descripción                                                 | Puntuación |
| ---------------------------- | ----------------------------------------------------------- | ---------- |
| Archivo docker-compose.yml   | Existe un archivo docker-compose.yml correctamente definido | 1          |
| Orquestación API + BD        | La API y PostgreSQL se ejecutan en contenedores separados   | 1          |
| Dependencias entre servicios | Uso correcto de `depends_on`                                | 0,5        |

---

### 4. Persistencia de datos con volúmenes (1,5 puntos)

| Criterio                | Descripción                                            | Puntuación |
| ----------------------- | ------------------------------------------------------ | ---------- |
| Uso de volúmenes        | La base de datos utiliza un volumen Docker             | 1          |
| Persistencia comprobada | Los datos se mantienen tras reiniciar los contenedores | 0,5        |

---

### 5. Creación automática de tablas (1 punto)

| Criterio               | Descripción                                               | Puntuación |
| ---------------------- | --------------------------------------------------------- | ---------- |
| Creación desde modelos | Las tablas se crean automáticamente desde los modelos ORM | 1          |

---

### 6. Despliegue en producción (1 punto)

| Criterio              | Descripción                                                           | Puntuación |
| --------------------- | --------------------------------------------------------------------- | ---------- |
| Aplicación desplegada | La aplicación está desplegada en Render (u otro servicio equivalente) | 1          |

---

## Criterios de calificación final

- 9 – 10 → Excelente (despliegue completo y correcto)
- 7 – 8,9 → Notable (pequeños detalles mejorables)
- 5 – 6,9 → Aprobado (funcional, pero incompleto)
- < 5 → Suspenso

---

## Observaciones

- La aplicación debe funcionar correctamente tanto en local como en producción.
- No se evaluará el diseño visual, sino el **correcto despliegue backend**.
- El uso de migraciones (Alembic) se valorará como mejora opcional.

---

## Mejoras opcionales (no obligatorias)

Estas mejoras no son obligatorias, pero pueden servir para subir nota:

- Uso de Alembic para migraciones
- Separación de entornos (desarrollo / producción)
- Uso de variables de entorno con archivo `.env`
- Documentación clara en el README
