from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MembresiaCreate(BaseModel):
    plan_id: int

class MembresiaResponse(BaseModel):
    id: int
    usuario_id: int
    plan_id: int
    fecha_inicio: datetime
    fecha_fin: datetime
    activa: bool

    class Config:
        from_attributes = True