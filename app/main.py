from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.models import usuario, plan, membresia, tiquetera, ingreso, face_encoding

Base.metadata.create_all(bind=engine)

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



