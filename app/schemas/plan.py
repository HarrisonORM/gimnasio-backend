from pydantic import BaseModel

class PlanBase(BaseModel):
    nombre: str
    duracion_dias: int
    precio: float

class PlanCreate(PlanBase):
    pass

class PlanResponse(PlanBase):
    id: int

    class Config:
        from_attributes = True