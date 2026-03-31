from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Ingreso(Base):
    __tablename__ = "ingresos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_hora = Column(DateTime, default=func.now())
    tipo_acceso = Column(String(20), nullable=True)
    permitido = Column(Boolean, nullable=False)
    motivo_denegado = Column(String(255), nullable=True)

    usuario = relationship("Usuario", back_populates="ingresos")