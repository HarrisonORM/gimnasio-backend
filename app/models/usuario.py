from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    cedula = Column(String(20), unique=True, nullable=True)
    foto_path = Column(String(255), nullable=True)
    fecha_registro = Column(DateTime, default=func.now())

    membresia = relationship("Membresia", back_populates="usuario", uselist=False)
    tiquetera = relationship("Tiquetera", back_populates="usuario", uselist=False)
    ingresos = relationship("Ingreso", back_populates="usuario")
    face_encoding = relationship("FaceEncoding", back_populates="usuario", uselist=False)