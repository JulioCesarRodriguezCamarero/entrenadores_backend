from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

DATABASE_URL = "mysql+mysqlconnector://root:julio@localhost/entrenamiento"


def get_engine(database_url):
    return create_engine(database_url)


def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Crear la base de datos 'entrenamiento' si no existe
def create_database_if_not_exists():
    # Conectar sin especificar la base de datos
    temp_engine = create_engine("mysql+mysqlconnector://root:julio@localhost")
    with temp_engine.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS entrenamiento"))
        print("Base de datos 'entrenamiento' verificada o creada.")
    temp_engine.dispose()


# Llamar a la función para asegurarnos de que la base de datos exista
create_database_if_not_exists()

engine = get_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)
Base = declarative_base()


def init_db():
    # Importar los modelos para que se registren adecuadamente
    from .models import Entrenador, Cliente, Nutricion, Rutina
    Base.metadata.create_all(bind=engine)


# Definir la función get_db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
