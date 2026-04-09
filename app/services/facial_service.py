import os
import numpy as np
import pickle
from deepface import DeepFace
from sqlalchemy.orm import Session
from app.models.face_encoding import FaceEncoding
from app.models.usuario import Usuario

MODELO = "Facenet"
DETECTOR = "opencv"

def extraer_embedding(imagen_path: str):
    try:
        resultado = DeepFace.represent(
            img_path=imagen_path,
            model_name=MODELO,
            detector_backend=DETECTOR,
            enforce_detection=True
        )
        embedding = resultado[0]["embedding"]
        return np.array(embedding)
    except Exception as e:
        print(f"Error extrayendo embedding: {e}")
        return None

def calcular_distancia(embedding1: np.ndarray, embedding2: np.ndarray):
    diferencia = embedding1 - embedding2
    distancia = np.sqrt(np.sum(diferencia ** 2))
    return distancia

def guardar_embedding(db: Session, usuario_id: int, embedding: np.ndarray):
    embedding_bytes = pickle.dumps(embedding)

    existente = db.query(FaceEncoding).filter(
        FaceEncoding.usuario_id == usuario_id
    ).first()

    if existente:
        existente.encoding = embedding_bytes
        db.commit()
        return existente

    db_encoding = FaceEncoding(
        usuario_id=usuario_id,
        encoding=embedding_bytes
    )
    db.add(db_encoding)
    db.commit()
    return db_encoding

def identificar_usuario(db: Session, imagen_path: str, umbral: float = 10.0):
    embedding_desconocido = extraer_embedding(imagen_path)
    if embedding_desconocido is None:
        return None, "No se detectó ningún rostro en la imagen"

    encodings_db = db.query(FaceEncoding).all()
    if not encodings_db:
        return None, "No hay usuarios registrados con reconocimiento facial"

    mejor_coincidencia = None
    mejor_distancia = float('inf')

    for registro in encodings_db:
        embedding_guardado = pickle.loads(registro.encoding)
        distancia = calcular_distancia(embedding_desconocido, embedding_guardado)

        if distancia < mejor_distancia:
            mejor_distancia = distancia
            mejor_coincidencia = registro

    print(f"Mejor distancia encontrada: {mejor_distancia:.2f}")

    if mejor_distancia <= umbral:
        usuario = db.query(Usuario).filter(
            Usuario.id == mejor_coincidencia.usuario_id
        ).first()
        return usuario, None

    return None, f"Rostro no reconocido — distancia: {mejor_distancia:.2f}"