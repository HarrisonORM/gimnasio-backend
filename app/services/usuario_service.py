from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate

def crear_usuario(db: Session, usuario: UsuarioCreate):
    db_usuario = Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        telefono=usuario.telefono,
        cedula=usuario.cedula
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Usuario).offset(skip).limit(limit).all()

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def obtener_usuario_por_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def actualizar_usuario(db: Session, usuario_id: int, usuario: UsuarioUpdate):
    db_usuario = obtener_usuario(db, usuario_id)
    if not db_usuario:
        return None
    if usuario.nombre is not None:
        db_usuario.nombre = usuario.nombre
    if usuario.apellido is not None:
        db_usuario.apellido = usuario.apellido
    if usuario.telefono is not None:
        db_usuario.telefono = usuario.telefono
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def eliminar_usuario(db: Session, usuario_id: int):
    db_usuario = obtener_usuario(db, usuario_id)
    if not db_usuario:
        return None
    db.delete(db_usuario)
    db.commit()
    return db_usuario