from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.models import usuario, plan, membresia, tiquetera, ingreso, face_encoding, admin
from app.routers import usuarios, planes, tiqueteras, acceso, dashboard, auth
from app.services.auth_service import crear_admin_inicial

Base.metadata.create_all(bind=engine)

db = SessionLocal()
crear_admin_inicial(db)
db.close()

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

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(planes.router)
app.include_router(tiqueteras.router)
app.include_router(acceso.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a Gimnasio API 💪"}

@app.get("/health")
def health():
    return {"status": "ok"}