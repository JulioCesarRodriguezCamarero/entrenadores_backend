#app/crud.py
from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models, schemas


# Funciones de CRUD

# Entrenador CRUD
def get_entrenadores(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Entrenador).offset(skip).limit(limit).all()


def get_entrenador(db: Session, entrenador_id: int):
    entrenador = db.query(models.Entrenador).filter(models.Entrenador.id == entrenador_id).first()
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador


def create_entrenador(db: Session, entrenador: schemas.EntrenadorCreate):
    db_entrenador = models.Entrenador(**entrenador.dict())
    db.add(db_entrenador)
    db.commit()
    db.refresh(db_entrenador)
    return db_entrenador


# Cliente CRUD
def get_clientes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Cliente).offset(skip).limit(limit).all()


def get_cliente(db: Session, cliente_id: int):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


def create_cliente(db: Session, cliente: schemas.ClienteCreate):
    db_cliente = models.Cliente(**cliente.dict())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


# Nutricion CRUD
def get_nutriciones(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Nutricion).offset(skip).limit(limit).all()


def create_nutricion(db: Session, nutricion: schemas.NutricionCreate):
    db_nutricion = models.Nutricion(**nutricion.dict())
    db.add(db_nutricion)
    db.commit()
    db.refresh(db_nutricion)
    return db_nutricion


# Rutina CRUD
def get_rutinas(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Rutina).offset(skip).limit(limit).all()


def create_rutina(db: Session, rutina: schemas.RutinaCreate):
    db_rutina = models.Rutina(**rutina.dict())
    db.add(db_rutina)
    db.commit()
    db.refresh(db_rutina)
    return db_rutina


# Funciones adicionales
def get_cliente_info(db: Session, cliente_id: int):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    entrenador = db.query(models.Entrenador).filter(models.Entrenador.id == db_cliente.entrenador_id).first()

    rutinas = db.query(models.Rutina).filter(models.Rutina.cliente_id == cliente_id).all()
    rutinas_info = [schemas.RutinaInfo(**rutina.__dict__) for rutina in rutinas]

    nutriciones = db.query(models.Nutricion).filter(models.Nutricion.cliente_id == cliente_id).all()
    nutricion_info = [schemas.NutricionInfo(**nutricion.__dict__) for nutricion in nutriciones]

    return schemas.ClienteInfo(
        cliente_id=db_cliente.id,
        cliente_nombre=db_cliente.nombre,
        entrenador=schemas.EntrenadorInfo(**entrenador.__dict__) if entrenador else None,
        rutinas=rutinas_info,
        nutricion=nutricion_info
    )
# Función para obtener un entrenador por su ID
def get_entrenador_by_id(db: Session, entrenador_id: int):
    entrenador = db.query(models.Entrenador).filter(models.Entrenador.id == entrenador_id).first()
    if not entrenador:
        raise HTTPException(status_code=404, detail="Entrenador no encontrado")
    return entrenador