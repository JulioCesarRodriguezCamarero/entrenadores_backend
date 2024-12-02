# app/db_check.py
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Ajusta la URL de la base de datos según tus parámetros
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/entrenamiento"

# Crear una instancia del motor (engine)
engine = create_engine(DATABASE_URL)

# Crear una clase SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def check_db_connection():
    try:
        # Iniciar una sesión
        db = SessionLocal()
        # Realizar una consulta simple para comprobar la conexión
        db.execute(text("SELECT 1"))
        print("Conexión a la base de datos exitosa")
    except SQLAlchemyError as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        db.close()


# Llamar a la función para verificar la conexión
if __name__ == "__main__":
    check_db_connection()
