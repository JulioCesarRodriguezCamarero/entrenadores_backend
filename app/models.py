# entrenamiento_web_app/app/models.py

from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship
from .database import Base


# Actualización de la clase Entrenador
class Entrenador(Base):
    __tablename__ = 'entrenadores'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(15), nullable=False)
    especialidad = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)  # Nueva columna
    clientes = relationship('Cliente', back_populates='entrenador')


# Actualización de la clase Cliente
class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(15), nullable=False)
    password = Column(String(100), nullable=False)  # Nueva columna
    entrenador_id = Column(Integer, ForeignKey('entrenadores.id'))
    entrenador = relationship('Entrenador', back_populates='clientes')
    nutricion = relationship('Nutricion', back_populates='cliente', uselist=False)
    rutinas = relationship('Rutina', back_populates='cliente')


class Nutricion(Base):
    __tablename__ = 'nutricion'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    plan_nutricional = Column(String(200), nullable=False)
    cliente = relationship('Cliente', back_populates='nutricion')


class Rutina(Base):
    __tablename__ = 'rutinas'
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(200), index=True)
    fecha = Column(Date)
    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship('Cliente', back_populates='rutinas')

