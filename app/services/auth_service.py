from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.models.admin import Admin
from app.config import SECRET_KEY

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def hashear_password(password: str):
    return pwd_context.hash(password)

def crear_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

def autenticar_admin(db: Session, username: str, password: str):
    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        return None
    if not verificar_password(password, admin.hashed_password):
        return None
    return admin

def crear_admin_inicial(db: Session):
    admin_existente = db.query(Admin).first()
    if not admin_existente:
        admin = Admin(
            username="admin",
            hashed_password=hashear_password("gimnasio123")
        )
        db.add(admin)
        db.commit()