#app/schemas.py
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class BaseUpdateModel(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None


class EntrenadorBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    especialidad: str
    password: str  # Nueva columna

    class Config:
        from_attributes = True  # Renombrado de orm_mode


class EntrenadorCreate(EntrenadorBase):
    pass


class EntrenadorUpdate(BaseUpdateModel):
    especialidad: Optional[str] = None


class Entrenador(EntrenadorBase):
    id: int

    class Config:
        from_attributes = True  # Renombrado de orm_mode


class ClienteBase(BaseModel):
    nombre: str
    email: str
    telefono: str
    entrenador_id: int
    password: str  # Nueva columna


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseUpdateModel):
    pass


class Cliente(ClienteBase):
    id: int

    class Config:
        from_attributes = True  # Renombrado de orm_mode


class NutricionBase(BaseModel):
    plan_nutricional: str


class NutricionCreate(NutricionBase):
    cliente_id: int


class NutricionUpdate(NutricionBase):
    plan_nutricional: Optional[str] = None


class Nutricion(NutricionBase):
    id: int
    cliente_id: int

    class Config:
        from_attributes = True  # Renombrado de orm_mode


class RutinaBase(BaseModel):
    descripcion: str
    fecha: date


class RutinaCreate(RutinaBase):
    cliente_id: int  # Asegura que este campo exista


class RutinaUpdate(BaseModel):
    descripcion: Optional[str] = None
    fecha: Optional[date] = None


class Rutina(RutinaBase):
    id: int
    cliente_id: int

    class Config:
        from_attributes = True  # Renombrado de orm_mode


class EntrenadorInfo(BaseModel):
    id: int
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    especialidad: Optional[str] = None
    password: Optional[str] = None


class RutinaInfo(BaseModel):
    id: int
    descripcion: str
    fecha: date = Field(..., description="Debe ser una fecha en el formato YYYY-MM-DD")

    @field_validator('fecha', mode='before')
    @classmethod
    def validate_fecha(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Fecha debe ser un formato de fecha válido en YYYY-MM-DD")
        elif isinstance(value, date):
            return value
        raise ValueError("Fecha debe ser una fecha válida")

    class Config:
        arbitrary_types_allowed = True


class NutricionInfo(BaseModel):
    id: int
    plan_nutricional: str


class ClienteInfo(BaseModel):
    cliente_id: int
    cliente_nombre: str
    entrenador: Optional[EntrenadorInfo]  # Permite que entrenador sea Optional
    rutinas: List[RutinaInfo]
    nutricion: List[NutricionInfo]

    class Config:
        from_attributes = True  # Renombrado de orm_mode
