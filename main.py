from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from models import models
from routes import categories, products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory API",
    description="API REST para gestión de inventario con FastAPI y SQLAlchemy",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173", # Vite default port
    # Add other origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(categories.router)
app.include_router(products.router)

@app.get("/")
def read_root():
    return {
        "message": "Bienvenido a la API de Inventario",
        "docs": "/docs",
        "endpoints": {
            "categories": "/categories",
            "products": "/products"
        }
    }
