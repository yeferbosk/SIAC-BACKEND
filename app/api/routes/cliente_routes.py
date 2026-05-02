from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.application.use_cases.cliente_service import ClienteService
from app.api.dependencies.db import get_cliente_service
from app.api.schemas.cliente_schema import ClienteSchema, ClienteCreate, ClienteUpdate
from app.domain.entities.cliente import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteSchema)
def crear_cliente(
    cliente: ClienteCreate,
    service: ClienteService = Depends(get_cliente_service),
):
    """
    Endpoint para registrar un nuevo cliente en el sistema.
    """
    # 1. Mapear datos del esquema a la entidad de dominio
    cliente_domain = Cliente(
        id_cliente=None,
        nombre=cliente.nombre,
        empresa=cliente.empresa,
        email=cliente.email,
        telefono=cliente.telefono,
        tipo_cliente=cliente.tipo_cliente
    )
    # 2. Llamar al servicio para realizar el registro
    return service.crear_cliente(cliente_domain)


@router.get("/", response_model=List[ClienteSchema])
def listar_clientes(
    service: ClienteService = Depends(get_cliente_service),
):
    """
    Endpoint para obtener la lista completa de clientes.
    """
    return service.listar_clientes()


@router.get("/{cliente_id}", response_model=ClienteSchema)
def obtener_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service),
):
    """
    Endpoint para obtener los detalles de un cliente específico por su ID.
    """
    # 1. Consultar al servicio
    cliente = service.obtener_cliente(cliente_id)
    # 2. Validar existencia
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{cliente_id}", response_model=ClienteSchema)
def actualizar_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    service: ClienteService = Depends(get_cliente_service),
):
    """
    Endpoint para actualizar los datos de un cliente. 
    Permite modificar todos los atributos excepto tipo_cliente y fecha_registro.
    """
    # 1. Verificar que el cliente existe antes de actualizar
    current = service.obtener_cliente(cliente_id)
    if not current:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    # 2. Actualizar solo los campos que vienen en la petición (Patch parcial)
    update_data = cliente.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current, key, value)
        
    # 3. Guardar cambios a través del servicio
    return service.actualizar_cliente(cliente_id, current)


@router.delete("/{cliente_id}")
def eliminar_cliente(
    cliente_id: int,
    service: ClienteService = Depends(get_cliente_service),
):
    """
    Endpoint para eliminar permanentemente un cliente del sistema.
    """
    # 1. Intentar eliminar a través del servicio
    exito = service.eliminar_cliente(cliente_id)
    # 2. Validar si se pudo realizar la operación
    if not exito:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return {"message": "Cliente eliminado con éxito"}