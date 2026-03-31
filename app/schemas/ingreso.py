from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class IngresoResponse(BaseModel):
    id: int
    usuario_id: int
    fecha_hora: datetime
    tipo_acceso: Optional[str] = None
    permitido: bool
    motivo_denegado: Optional[str] = None

    class Config:
        from_attributes = True