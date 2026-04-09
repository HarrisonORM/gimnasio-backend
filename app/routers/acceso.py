from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.ingreso import IngresoResponse
from app.services import acceso_service, usuario_service
from app.models.ingreso import Ingreso
from app.models.usuario import Usuario
from datetime import datetime

router = APIRouter(tags=["Acceso"])

@router.post("/acceso/{usuario_id}")
def registrar_acceso(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    resultado = acceso_service.validar_acceso(db, usuario_id)
    resultado["usuario"] = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido
    }
    return resultado

@router.get("/ingresos", response_model=List[IngresoResponse])
def listar_ingresos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return db.query(Ingreso).order_by(
        Ingreso.fecha_hora.desc()
    ).offset(skip).limit(limit).all()

@router.get("/ingresos/{usuario_id}", response_model=List[IngresoResponse])
def historial_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return db.query(Ingreso).filter(
        Ingreso.usuario_id == usuario_id
    ).order_by(Ingreso.fecha_hora.desc()).limit(20).all()
@router.post("/acceso/cedula/{cedula}")
def acceso_por_cedula(cedula: str, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.cedula == cedula
    ).first()

    if not usuario:
        return {
            "permitido": False,
            "mensaje": "Cédula no registrada en el sistema",
            "usuario": None
        }

    resultado = acceso_service.validar_acceso(db, usuario.id)
    resultado["usuario"] = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido
    }
    return resultado