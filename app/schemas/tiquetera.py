from pydantic import BaseModel, computed_field
from datetime import datetime

class TiqueteraCreate(BaseModel):
    pass

class TiqueteraResponse(BaseModel):
    id: int
    usuario_id: int
    entradas_totales: int
    entradas_usadas: int
    fecha_inicio: datetime
    fecha_vencimiento: datetime
    activa: bool

    @computed_field
    @property
    def entradas_disponibles(self) -> int:
        return self.entradas_totales - self.entradas_usadas

    class Config:
        from_attributes = True