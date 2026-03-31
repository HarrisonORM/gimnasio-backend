from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Membresia(Base):
    __tablename__ = "membresias"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("planes.id"), nullable=False)
    fecha_inicio = Column(DateTime, default=func.now())
    fecha_fin = Column(DateTime, nullable=False)
    activa = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="membresia")
    plan = relationship("Plan", back_populates="membresias")