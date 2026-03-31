from sqlalchemy.orm import Session
from datetime import datetime
from app.models.ingreso import Ingreso
from app.services import membresia_service, tiquetera_service

def validar_acceso(db: Session, usuario_id: int):
    membresia = membresia_service.verificar_y_actualizar_membresia(db, usuario_id)
    if membresia:
        ingreso = Ingreso(
            usuario_id=usuario_id,
            fecha_hora=datetime.now(),
            tipo_acceso="membresia",
            permitido=True,
            motivo_denegado=None
        )
        db.add(ingreso)
        db.commit()
        db.refresh(ingreso)
        return {
            "permitido": True,
            "tipo_acceso": "membresia",
            "mensaje": "Acceso permitido por membresía activa",
            "fecha_fin": membresia.fecha_fin,
            "ingreso_id": ingreso.id
        }

    tiquetera = tiquetera_service.verificar_tiquetera(db, usuario_id)
    if tiquetera:
        tiquetera_service.descontar_entrada(db, usuario_id)
        tiquetera_actualizada = tiquetera_service.obtener_tiquetera_activa(db, usuario_id)
        entradas_restantes = tiquetera.entradas_totales - tiquetera.entradas_usadas - 1

        ingreso = Ingreso(
            usuario_id=usuario_id,
            fecha_hora=datetime.now(),
            tipo_acceso="tiquetera",
            permitido=True,
            motivo_denegado=None
        )
        db.add(ingreso)
        db.commit()
        db.refresh(ingreso)
        return {
            "permitido": True,
            "tipo_acceso": "tiquetera",
            "mensaje": f"Acceso permitido. Te quedan {entradas_restantes} entradas",
            "entradas_restantes": entradas_restantes,
            "ingreso_id": ingreso.id
        }

    ingreso = Ingreso(
        usuario_id=usuario_id,
        fecha_hora=datetime.now(),
        tipo_acceso=None,
        permitido=False,
        motivo_denegado="Sin membresía activa ni entradas disponibles"
    )
    db.add(ingreso)
    db.commit()
    return {
        "permitido": False,
        "tipo_acceso": None,
        "mensaje": "Acceso denegado - Sin membresía activa ni entradas disponibles"
    }