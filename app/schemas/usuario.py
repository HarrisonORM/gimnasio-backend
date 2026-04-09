from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str] = None
    cedula: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    cedula: Optional[str] = None

class UsuarioResponse(UsuarioBase):
    id: int
    foto_path: Optional[str] = None
    fecha_registro: datetime

    class Config:
        from_attributes = True