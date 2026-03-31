from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.tiquetera import TiqueteraResponse
from app.services import tiquetera_service, usuario_service

router = APIRouter(tags=["Tiqueteras"])

@router.post("/usuarios/{usuario_id}/tiquetera", response_model=TiqueteraResponse)
def crear_tiquetera(usuario_id: int, db: Session = Depends(get_db)):
    usuario = usuario_service.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    tiquetera = tiquetera_service.crear_tiquetera(db, usuario_id)
    if not tiquetera:
        raise HTTPException(
            status_code=400,
            detail="Este usuario ya tiene una tiquetera activa"
        )
    return tiquetera

@router.get("/usuarios/{usuario_id}/tiquetera", response_model=TiqueteraResponse)
def ver_tiquetera(usuario_id: int, db: Session = Depends(get_db)):
    tiquetera = tiquetera_service.verificar_tiquetera(db, usuario_id)
    if not tiquetera:
        raise HTTPException(
            status_code=404,
            detail="Este usuario no tiene una tiquetera activa"
        )
    return tiquetera