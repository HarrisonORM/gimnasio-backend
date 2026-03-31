from sqlalchemy.orm import Session
from app.models.plan import Plan

def obtener_planes(db: Session):
    return db.query(Plan).all()

def obtener_plan(db: Session, plan_id: int):
    return db.query(Plan).filter(Plan.id == plan_id).first()