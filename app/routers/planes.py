from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.plan import PlanResponse
from app.schemas.membresia import MembresiaCreate, MembresiaResponse
from app.services import plan_service, membresia_service
from app.services import usuario_service

router = APIRouter(tags=["Planes y Membresías"])

@router.get("/planes", response_model=List[PlanResponse])
def listar_planes(db: Session = Depends(get_db)):
    return plan_service.obtener_planes(db)

@router.get("/planes/{plan_id}", response_model=PlanResponse)
def obtener_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = plan_service.obtener_plan(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return plan

@router.post("/usuarios/{usuario_id}/membresia", response_model=MembresiaResponse)
def asignar_membresia(usuario_id: int, membresia: MembresiaCreate, db: Session = Depends(get_db)):
    usuario = usuario_service.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    plan = plan_service.obtener_plan(db, membresia.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan no encontrado")

    if plan.nombre == "Tiquetera":
        raise HTTPException(
            status_code=400,
            detail="Para tiqueteras usa el endpoint /usuarios/{id}/tiquetera"
        )

    db_membresia = membresia_service.crear_membresia(db, usuario_id, membresia)
    return db_membresia

@router.get("/usuarios/{usuario_id}/membresia", response_model=MembresiaResponse)
def ver_membresia(usuario_id: int, db: Session = Depends(get_db)):
    membresia = membresia_service.verificar_y_actualizar_membresia(db, usuario_id)
    if not membresia:
        raise HTTPException(
            status_code=404,
            detail="Este usuario no tiene una membresía activa"
        )
    return membresia