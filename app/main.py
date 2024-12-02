# entrenamiento_web_app/app/main.py

import logging
from datetime import datetime, timedelta
from typing import List

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from . import crud, models, schemas
from .database import engine
from .routers import cliente_router  # Asegúrate de que el nombre del módulo y el router sean correctos
from .security import hash_password, verify_password

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Crear la aplicación principal de FastAPI
app = FastAPI()

# Configurar el logging para obtener información de depuración
logging.basicConfig(level=logging.INFO)

# Configurar CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir orígenes específicos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todas las cabeceras
)

SECRET_KEY = "la_llave_de_Ane"  # Cámbialo a una cadena secreta segura
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Incluye el router del cliente
app.include_router(cliente_router.router)


# Funciones para JWT
def create_jwt(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded if decoded["exp"] >= datetime.utcnow() else None
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    decoded_token = decode_jwt(token)
    if decoded_token is None:
        raise credentials_exception
    email = decoded_token.get("sub")
    if email is None:
        raise credentials_exception
    user = db.query(models.Entrenador).filter(models.Entrenador.email == email).first()
    if user is None:
        raise credentials_exception
    return user


# Ruta básica para verificar que el servidor está funcionando correctamente
@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}


# Endpoints para autenticación
@app.post("/login_entrenador/")
def login_entrenador(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Entrenador).filter(models.Entrenador.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    jwt_token = create_jwt({"sub": user.email})
    return {
        "entrenador_id":user.id,
        "access_token": jwt_token,
        "token_type": "bearer"}


@app.post("/login_cliente/")
def login_cliente(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.Cliente).filter(models.Cliente.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    jwt_token = create_jwt({"sub": user.email})
    return {
        "cliente_id": user.id,  # Asegúrate de que `id` es el campo del cliente que almacena el ID
        "access_token": jwt_token,
        "token_type": "bearer"
    }


# Entrenador Endpoints
@app.post("/entrenadores/", response_model=schemas.Entrenador)
def register_or_create_entrenador(entrenador: schemas.EntrenadorCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(entrenador.password)
    db_entrenador = models.Entrenador(
        nombre=entrenador.nombre,
        email=entrenador.email,
        telefono=entrenador.telefono,
        especialidad=entrenador.especialidad,
        password=hashed_password
    )
    db.add(db_entrenador)
    db.commit()
    db.refresh(db_entrenador)
    return db_entrenador


@app.get("/entrenadores/", response_model=List[schemas.Entrenador])
def read_entrenadores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    entrenadores = crud.get_entrenadores(db, skip=skip, limit=limit)
    return entrenadores


@app.get("/entrenadores/{entrenador_id}", response_model=schemas.Entrenador)
def read_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    db_entrenador = crud.get_entrenador(db, entrenador_id=entrenador_id)
    if db_entrenador is None:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return db_entrenador


@app.put("/entrenadores/{entrenador_id}", response_model=schemas.Entrenador)
def update_entrenador(entrenador_id: int, entrenador: schemas.EntrenadorUpdate, db: Session = Depends(get_db)):
    return crud.update_entrenador(db=db, entrenador_id=entrenador_id, entrenador=entrenador)


@app.delete("/entrenadores/{entrenador_id}", response_model=schemas.Entrenador)
def delete_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    return crud.delete_entrenador(db=db, entrenador_id=entrenador_id)


# Cliente Endpoints
@app.post("/clientes/", response_model=schemas.Cliente)
def register_or_create_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(cliente.password)
    db_cliente = models.Cliente(
        nombre=cliente.nombre,
        email=cliente.email,
        telefono=cliente.telefono,
        password=hashed_password,
        entrenador_id=cliente.entrenador_id,
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


@app.get("/clientes/", response_model=List[schemas.Cliente])
def read_clientes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clientes = crud.get_clientes(db, skip=skip, limit=limit)
    return clientes


@app.get("/clientes/{cliente_id}", response_model=schemas.Cliente)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    db_cliente = crud.get_cliente(db, cliente_id=cliente_id)
    if db_cliente is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_cliente


@app.put("/clientes/{cliente_id}", response_model=schemas.Cliente)
def update_cliente(cliente_id: int, cliente: schemas.ClienteUpdate, db: Session = Depends(get_db)):
    return crud.update_cliente(db=db, cliente_id=cliente_id, cliente=cliente)


@app.delete("/clientes/{cliente_id}", response_model=schemas.Cliente)
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return crud.delete_cliente(db=db, cliente_id=cliente_id)


# Rutina Endpoints
@app.get("/rutinas/", response_model=List[schemas.Rutina])
def read_rutinas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    rutinas = db.query(models.Rutina).offset(skip).limit(limit).all()
    return rutinas


@app.post("/rutinas/", response_model=schemas.Rutina)
def create_rutina(rutina: schemas.RutinaCreate, db: Session = Depends(get_db)):
    return crud.create_rutina(db=db, rutina=rutina)


@app.put("/rutinas/{rutina_id}", response_model=schemas.Rutina)
def update_rutina(rutina_id: int, rutina: schemas.RutinaUpdate, db: Session = Depends(get_db)):
    return crud.update_rutina(db=db, rutina_id=rutina_id, rutina=rutina)


@app.delete("/rutinas/{rutina_id}", response_model=schemas.Rutina)
def delete_rutina(rutina_id: int, db: Session = Depends(get_db)):
    return crud.delete_rutina(db=db, rutina_id=rutina_id)


# Nutricion Endpoints
@app.get("/nutriciones/", response_model=List[schemas.Nutricion])
def read_nutriciones(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    nutriciones = crud.get_nutriciones(db, skip=skip, limit=limit)
    return nutriciones


@app.post("/nutriciones/", response_model=schemas.Nutricion)
def create_nutricion(nutricion: schemas.NutricionCreate, db: Session = Depends(get_db)):
    return crud.create_nutricion(db=db, nutricion=nutricion)


@app.put("/nutriciones/{nutricion_id}", response_model=schemas.Nutricion)
def update_nutricion(nutricion_id: int, nutricion: schemas.NutricionUpdate, db: Session = Depends(get_db)):
    return crud.update_nutricion(db=db, nutricion_id=nutricion_id, nutricion=nutricion)


@app.delete("/nutriciones/{nutricion_id}", response_model=schemas.Nutricion)
def delete_nutricion(nutricion_id: int, db: Session = Depends(get_db)):
    return crud.delete_nutricion(db=db, nutricion_id=nutricion_id)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
