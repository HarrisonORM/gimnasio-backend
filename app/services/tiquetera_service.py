from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.tiquetera import Tiquetera

def obtener_tiquetera_activa(db: Session, usuario_id: int):
    return db.query(Tiquetera).filter(
        Tiquetera.usuario_id == usuario_id,
        Tiquetera.activa == True
    ).first()

def crear_tiquetera(db: Session, usuario_id: int):
    tiquetera_existente = obtener_tiquetera_activa(db, usuario_id)
    if tiquetera_existente:
        return None

    fecha_inicio = datetime.now()
    fecha_vencimiento = fecha_inicio + timedelta(days=60)

    db_tiquetera = Tiquetera(
        usuario_id=usuario_id,
        entradas_totales=15,
        entradas_usadas=0,
        fecha_inicio=fecha_inicio,
        fecha_vencimiento=fecha_vencimiento,
        activa=True
    )
    db.add(db_tiquetera)
    db.commit()
    db.refresh(db_tiquetera)
    return db_tiquetera

def verificar_tiquetera(db: Session, usuario_id: int):
    tiquetera = obtener_tiquetera_activa(db, usuario_id)
    if not tiquetera:
        return None
    if datetime.now() > tiquetera.fecha_vencimiento:
        tiquetera.activa = False
        db.commit()
        return None
    if tiquetera.entradas_usadas >= tiquetera.entradas_totales:
        tiquetera.activa = False
        db.commit()
        return None
    return tiquetera

def descontar_entrada(db: Session, usuario_id: int):
    tiquetera = verificar_tiquetera(db, usuario_id)
    if not tiquetera:
        return None
    tiquetera.entradas_usadas += 1
    if tiquetera.entradas_usadas >= tiquetera.entradas_totales:
        tiquetera.activa = False
    db.commit()
    db.refresh(tiquetera)
    return tiquetera