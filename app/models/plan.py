from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    duracion_dias = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)

    membresias = relationship("Membresia", back_populates="plan")