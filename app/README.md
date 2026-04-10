# EvoGym — Backend

Sistema de gestión para gimnasio con reconocimiento facial automático.
Desarrollado con Python y FastAPI.

---

## ¿Qué hace este sistema?

- Registra y gestiona los miembros del gimnasio
- Controla el acceso por reconocimiento facial automático
- Permite el ingreso alternativo por número de cédula
- Gestiona membresías mensuales, bimestrales, trimestrales, semestrales y anuales
- Gestiona tiqueteras de 15 entradas con vigencia de 2 meses
- Muestra estadísticas en tiempo real para el administrador
- Envía alertas cuando una membresía está próxima a vencer

---

## Requisitos previos

Antes de instalar, asegúrate de tener esto en tu computador:

- Python 3.11 o superior
- PostgreSQL 16 o superior
- Git

---

## Instalación paso a paso

1. Clona el proyecto

git clone https://github.com/TU_USUARIO/gimnasio-backend.git
cd gimnasio-backend

2. Crea el entorno virtual

python -m venv venv

3. Actívalo

En Windows:
venv\Scripts\activate

En Mac/Linux:
source venv/bin/activate

4. Instala las librerías

pip install -r requirements.txt

5. Crea la base de datos

Abre pgAdmin y crea una base de datos llamada gimnasio_db.

6. Configura las variables de entorno

Crea un archivo .env en la raíz del proyecto con este contenido:

DATABASE_URL=postgresql://postgres:******@localhost:5432/gimnasio_db
SECRET_KEY= *123***321*

Reemplaza TU_PASSWORD por la contraseña de tu PostgreSQL.
Para generar una clave secreta segura corre:
python -c "import secrets; print(secrets.token_hex(32))"

7. Inicia el servidor

python -m uvicorn app.main:app --reload

El servidor queda disponible en: http://localhost:8000

---

## Credenciales del administrador

Al iniciar el servidor por primera vez se crea automáticamente un administrador:

Usuario: admin
Contraseña: gimnasio123

Se recomienda cambiar la contraseña después del primer inicio.

---

## Documentación de la API

Una vez corriendo el servidor puedes ver y probar todos los endpoints en:
http://localhost:8000/docs

---

## Estructura del proyecto

gimnasio-backend/
├── app/
│   ├── models/       — Estructura de la base de datos
│   ├── schemas/      — Validación de datos
│   ├── routers/      — Endpoints de la API
│   ├── services/     — Lógica del negocio
│   └── main.py       — Punto de entrada
├── media/            — Fotos de los usuarios (no se sube a GitHub)
├── .env              — Variables privadas (no se sube a GitHub)
└── requirements.txt  — Librerías necesarias

---

## Tecnologías utilizadas

FastAPI        — Framework del servidor
PostgreSQL     — Base de datos
SQLAlchemy     — Conexión con la base de datos
DeepFace       — Reconocimiento facial
JWT            — Autenticación segura
bcrypt         — Encriptación de contraseñas

---

## ¿Problemas comunes?

El servidor no inicia:
Verifica que el entorno virtual esté activo. Debes ver (venv) al inicio de la terminal.

Error de conexión a la base de datos:
Verifica que PostgreSQL esté corriendo y que la contraseña en el .env sea correcta.

El reconocimiento facial no funciona:
Asegúrate de tener buena iluminación y que el usuario tenga una foto registrada.