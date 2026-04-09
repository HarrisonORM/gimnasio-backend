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

        dias_restantes = (membresia.fecha_fin - datetime.now()).days
        return {
            "permitido": True,
            "tipo_acceso": "membresia",
            "mensaje_bienvenida": "Bienvenido a EVOGYM",
            "mensaje": f"Membresía activa — vence en {dias_restantes} días",
            "fecha_fin": membresia.fecha_fin,
            "ingreso_id": ingreso.id
        }

    tiquetera = tiquetera_service.verificar_tiquetera(db, usuario_id)
    if tiquetera:
        tiquetera_service.descontar_entrada(db, usuario_id)
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
            "mensaje_bienvenida": "Bienvenido a EVOGYM",
            "mensaje": f"Te quedan {entradas_restantes} entradas disponibles",
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
        "mensaje_bienvenida": None,
        "mensaje": "No tienes membresía activa ni entradas disponibles"
    }