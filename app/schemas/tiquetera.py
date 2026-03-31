from pydantic import BaseModel
from datetime import datetime

class TiqueteraCreate(BaseModel):
    pass

class TiqueteraResponse(BaseModel):
    id: int
    usuario_id: int
    entradas_totales: int
    entradas_usadas: int
    entradas_disponibles: int
    fecha_inicio: datetime
    fecha_vencimiento: datetime
    activa: bool

    class Config:
        from_attributes = True