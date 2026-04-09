import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import facial_service, acceso_service, usuario_service

router = APIRouter(prefix="/facial", tags=["Reconocimiento Facial"])

MEDIA_DIR = "media/fotos"

def guardar_archivo_temporal(file_content: bytes, extension: str) -> str:
    os.makedirs(MEDIA_DIR, exist_ok=True)
    nombre = f"temp_{uuid.uuid4().hex}.{extension}"
    ruta = os.path.join(MEDIA_DIR, nombre)
    with open(ruta, "wb") as f:
        f.write(file_content)
    return ruta

@router.post("/registrar/{usuario_id}")
async def registrar_facial(
    usuario_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    usuario = usuario_service.obtener_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    contenido = await file.read()
    ruta_temp = guardar_archivo_temporal(contenido, extension)

    try:
        embedding = facial_service.extraer_embedding(ruta_temp)
        if embedding is None:
            raise HTTPException(
                status_code=400,
                detail="No se detectó ningún rostro. Intenta con mejor iluminación."
            )

        facial_service.guardar_embedding(db, usuario_id, embedding)

        ruta_foto = os.path.join(MEDIA_DIR, f"foto_{usuario_id}.{extension}")
        os.rename(ruta_temp, ruta_foto)

        db_usuario = usuario_service.obtener_usuario(db, usuario_id)
        db_usuario.foto_path = ruta_foto
        db.commit()

        return {
            "mensaje": "Reconocimiento facial registrado exitosamente",
            "usuario_id": usuario_id,
            "foto_path": ruta_foto
        }
    except HTTPException:
        raise
    except Exception as e:
        if os.path.exists(ruta_temp):
            os.remove(ruta_temp)
        raise HTTPException(status_code=500, detail=f"Error procesando imagen: {str(e)}")

@router.post("/identificar")
async def identificar(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    contenido = await file.read()
    ruta_temp = guardar_archivo_temporal(contenido, extension)

    try:
        usuario, motivo = facial_service.identificar_usuario(db, ruta_temp)
    except Exception as e:
        if os.path.exists(ruta_temp):
            os.remove(ruta_temp)
        return {
            "permitido": False,
            "mensaje": f"Error procesando imagen: {str(e)}",
            "usuario": None
        }
    finally:
        if os.path.exists(ruta_temp):
            os.remove(ruta_temp)

    if not usuario:
        return {
            "permitido": False,
            "mensaje": motivo or "Usuario no reconocido",
            "usuario": None
        }

    resultado = acceso_service.validar_acceso(db, usuario.id)
    resultado["usuario"] = {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido
    }
    return resultado