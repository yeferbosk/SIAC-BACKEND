from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.use_cases.transformador_service import TransformadorService
from app.api.dependencies.db import get_transformador_service
from app.api.schemas.transformador_schema import TransformadorSchema, TransformadorCreate, TransformadorUpdate
from app.domain.entities.transformador import Transformador

router = APIRouter(prefix="/transformadores", tags=["Transformadores"])

@router.post("/", response_model=TransformadorSchema)
def crear_transformador(
    t: TransformadorCreate, 
    service: TransformadorService = Depends(get_transformador_service)
):
    """
    Registra un nuevo transformador en el inventario técnico del SIAC.
    """
    # 1. Crear instancia de dominio con los datos del esquema
    t_domain = Transformador(
        id_transformador=None,
        referencia=t.referencia,
        tipo=t.tipo,
        potencia_kva=t.potencia_kva,
        tension_primaria=t.tension_primaria,
        tension_secundaria=t.tension_secundaria,
        material_bobinado=t.material_bobinado,
        estado=t.estado,
        stock_disponible=t.stock_disponible,
        precio_venta=t.precio_venta,
        precio_alquiler_dia=t.precio_alquiler_dia
    )
    # 2. Guardar en DB a través del servicio
    return service.crear_transformador(t_domain)

@router.get("/", response_model=List[TransformadorSchema])
def listar_transformadores(service: TransformadorService = Depends(get_transformador_service)):
    """
    Obtiene la lista de todos los transformadores registrados.
    """
    return service.listar_transformadores()

@router.get("/{t_id}", response_model=TransformadorSchema)
def obtener_transformador(
    t_id: int, 
    service: TransformadorService = Depends(get_transformador_service)
):
    """
    Consulta los detalles técnicos de un transformador específico.
    """
    t = service.obtener_transformador(t_id)
    if not t:
        raise HTTPException(status_code=404, detail="Transformador no encontrado")
    return t

@router.put("/{t_id}", response_model=TransformadorSchema)
def actualizar_transformador(
    t_id: int,
    t_update: TransformadorUpdate,
    service: TransformadorService = Depends(get_transformador_service)
):
    """
    Permite editar cualquier atributo técnico o comercial de un transformador existente.
    """
    # 1. Verificar existencia
    current = service.obtener_transformador(t_id)
    if not current:
        raise HTTPException(status_code=404, detail="Transformador no encontrado")
    
    # 2. Aplicar cambios parciales
    update_data = t_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current, key, value)
    
    # 3. Guardar cambios
    return service.actualizar_transformador(t_id, current)

@router.delete("/{t_id}")
def eliminar_transformador(
    t_id: int,
    service: TransformadorService = Depends(get_transformador_service)
):
    """
    Elimina físicamente un transformador del sistema.
    """
    if not service.eliminar_transformador(t_id):
        raise HTTPException(status_code=404, detail="Transformador no encontrado")
    return {"message": "Transformador eliminado del sistema correctamente"}
