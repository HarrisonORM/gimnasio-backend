from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Tiquetera(Base):
    __tablename__ = "tiqueteras"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    entradas_totales = Column(Integer, default=15)
    entradas_usadas = Column(Integer, default=0)
    fecha_inicio = Column(DateTime, default=func.now())
    fecha_vencimiento = Column(DateTime, nullable=False)
    activa = Column(Boolean, default=True)

    usuario = relationship("Usuario", back_populates="tiquetera")