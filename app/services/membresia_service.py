from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.membresia import Membresia
from app.models.plan import Plan
from app.schemas.membresia import MembresiaCreate

def obtener_membresia_activa(db: Session, usuario_id: int):
    return db.query(Membresia).filter(
        Membresia.usuario_id == usuario_id,
        Membresia.activa == True
    ).first()

def crear_membresia(db: Session, usuario_id: int, membresia: MembresiaCreate):
    plan = db.query(Plan).filter(Plan.id == membresia.plan_id).first()
    if not plan:
        return None

    membresia_existente = obtener_membresia_activa(db, usuario_id)
    if membresia_existente:
        membresia_existente.activa = False
        db.commit()

    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=plan.duracion_dias)

    db_membresia = Membresia(
        usuario_id=usuario_id,
        plan_id=plan.id,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        activa=True
    )
    db.add(db_membresia)
    db.commit()
    db.refresh(db_membresia)
    return db_membresia

def verificar_y_actualizar_membresia(db: Session, usuario_id: int):
    membresia = obtener_membresia_activa(db, usuario_id)
    if not membresia:
        return None
    if datetime.now() > membresia.fecha_fin:
        membresia.activa = False
        db.commit()
        return None
    return membresia