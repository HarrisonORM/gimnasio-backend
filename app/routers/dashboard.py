from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.models.usuario import Usuario
from app.models.membresia import Membresia
from app.models.ingreso import Ingreso

router = APIRouter(tags=["Dashboard"])

@router.get("/dashboard")
def obtener_estadisticas(db: Session = Depends(get_db)):
    total_usuarios = db.query(Usuario).count()

    membresias_activas = db.query(Membresia).filter(
        Membresia.activa == True,
        Membresia.fecha_fin > datetime.now()
    ).count()

    ingresos_hoy = db.query(Ingreso).filter(
        Ingreso.fecha_hora >= datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        ),
        Ingreso.permitido == True
    ).count()

    return {
        "total_usuarios": total_usuarios,
        "membresias_activas": membresias_activas,
        "ingresos_hoy": ingresos_hoy,
    }

@router.get("/alertas")
def obtener_alertas(db: Session = Depends(get_db)):
    en_5_dias = datetime.now() + timedelta(days=5)

    membresias_por_vencer = db.query(Membresia).filter(
        Membresia.activa == True,
        Membresia.fecha_fin <= en_5_dias,
        Membresia.fecha_fin > datetime.now()
    ).all()

    alertas = []
    for membresia in membresias_por_vencer:
        usuario = db.query(Usuario).filter(
            Usuario.id == membresia.usuario_id
        ).first()

        dias_restantes = (membresia.fecha_fin - datetime.now()).days
        alertas.append({
            "usuario_id": membresia.usuario_id,
            "nombre_completo": f"{usuario.nombre} {usuario.apellido}" if usuario else f"Usuario #{membresia.usuario_id}",
            "dias_restantes": dias_restantes,
            "fecha_fin": membresia.fecha_fin,
            "mensaje": f"Membresía vence en {dias_restantes} días"
        })

    return {"alertas": alertas, "total": len(alertas)}

@router.get("/ingresos")
def listar_ingresos(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    ingresos = db.query(Ingreso).order_by(
        Ingreso.fecha_hora.desc()
    ).offset(skip).limit(limit).all()

    resultado = []
    for ingreso in ingresos:
        usuario = None
        if ingreso.usuario_id:
            usuario = db.query(Usuario).filter(
                Usuario.id == ingreso.usuario_id
            ).first()

        resultado.append({
            "id": ingreso.id,
            "usuario_id": ingreso.usuario_id,
            "nombre_completo": f"{usuario.nombre} {usuario.apellido}" if usuario else "Desconocido",
            "fecha_hora": ingreso.fecha_hora,
            "tipo_acceso": ingreso.tipo_acceso,
            "permitido": ingreso.permitido,
            "motivo_denegado": ingreso.motivo_denegado
        })

    return resultado