# app/routers/cliente_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import get_db
import logging

router = APIRouter()


@router.get("/clientes_info/{cliente_id}/", response_model=schemas.ClienteInfo)
def get_clientes_info(cliente_id: int, db: Session = Depends(get_db)):
    logging.info(f"Iniciando consulta para cliente_id: {cliente_id}")

    try:
        # Obtener la información del cliente usando la función crud
        response = crud.get_cliente_info(db, cliente_id)
        logging.info(f"Información del cliente obtenida: {response}")
    except HTTPException as e:
        logging.warning(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"Error al obtener las relaciones del cliente: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return response


# Endpoint para obtener todos los clientes de un entrenador
@router.get("/entrenadores/{entrenador_id}/clientes", response_model=List[schemas.Cliente])
def get_clientes_by_entrenador(entrenador_id: int, db: Session = Depends(get_db)):
    logging.info(f"Iniciando consulta de clientes para entrenador_id: {entrenador_id}")

    try:
        # Obtener el entrenador y verificar su existencia
        entrenador = crud.get_entrenador_by_id(db, entrenador_id)  # Asumiendo que tienes una función CRUD similar
        if not entrenador:
            logging.warning(f"Entrenador no encontrado: {entrenador_id}")
            raise HTTPException(status_code=404, detail="Entrenador no encontrado")

        # Obtener los clientes relacionados al entrenador
        clientes = entrenador.clientes
        logging.info(f"Clientes obtenidos para el entrenador {entrenador_id}: {clientes}")

    except HTTPException as e:
        logging.warning(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logging.error(f"Error al obtener los clientes del entrenador: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")

    return clientes