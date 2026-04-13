from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.models import usuario, plan, membresia, tiquetera, ingreso, face_encoding, admin
from app.routers import usuarios, planes, tiqueteras, acceso, dashboard, auth, facial
from app.services.auth_service import crear_admin_inicial
from app.routers import usuarios, planes, tiqueteras, acceso, dashboard, auth, facial
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
    allow_origins=[
        "http://localhost:5173",
        "https://gimnasio-frontend-tau.vercel.app"
    ],
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
app.include_router(facial.router)
@app.get("/")
def root():
    return {"mensaje": "Bienvenido a Gimnasio API 💪"}

@app.get("/health")
def health():
    return {"status": "ok"}
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)