from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.services import usuario_service

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    email_existente = usuario_service.obtener_usuario_por_email(db, usuario.email)
    if email_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con ese email"
        )
    return usuario_service.crear_usuario(db, usuario)

@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return usuario_service.obtener_usuarios(db, skip, limit)

@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuario_service.obtener_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return db_usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    db_usuario = usuario_service.actualizar_usuario(db, usuario_id, usuario)
    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )
    return db_usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = usuario_service.eliminar_usuario(db, usuario_id)
    if not db_usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )