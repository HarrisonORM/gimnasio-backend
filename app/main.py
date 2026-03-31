from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Gimnasio API",
    description="Sistema de gestión de gimnasio con reconocimiento facial",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a Gimnasio API 💪"}

@app.get("/health")
def health():
    return {"status": "ok"}

from app.database import engine

@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as connection:
            return {"database": "conexion exitosa ✅"}
    except Exception as e:
        return {"database": f"error: {str(e)}"}