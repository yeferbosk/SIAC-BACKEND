from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.use_cases.empleado_service import EmpleadoService
from app.api.dependencies.services import get_empleado_service
from app.api.schemas.empleado_schema import EmpleadoSchema, EmpleadoCreate, EmpleadoUpdate
from app.domain.entities.empleado import Empleado

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=EmpleadoSchema)
def crear_empleado(
    empleado: EmpleadoCreate, 
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Registra un nuevo empleado en el SIAC.
    """
    # 1. Crear entidad de dominio
    emp_domain = Empleado(
        id_empleado=None,
        nombre=empleado.nombre,
        email=empleado.email,
        password=empleado.password,
        rol=empleado.rol,
        area=empleado.area,
        activo=empleado.activo
    )
    # 2. Persistir
    return service.crear_empleado(emp_domain)

@router.get("/", response_model=List[EmpleadoSchema])
def listar_empleados(service: EmpleadoService = Depends(get_empleado_service)):
    """
    Retorna la lista de todos los empleados.
    """
    return service.listar_empleados()

@router.get("/{empleado_id}", response_model=EmpleadoSchema)
def obtener_empleado(
    empleado_id: int, 
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Obtiene detalles de un empleado por su ID.
    """
    emp = service.obtener_empleado(empleado_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return emp

@router.put("/{empleado_id}", response_model=EmpleadoSchema)
def actualizar_empleado(
    empleado_id: int,
    empleado: EmpleadoUpdate,
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Actualiza la información de un empleado (nombre, email, rol, area, activo).
    """
    # 1. Buscar registro actual
    current = service.obtener_empleado(empleado_id)
    if not current:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    # 2. Mapear cambios
    update_data = empleado.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current, key, value)
    
    # 3. Guardar cambios
    return service.actualizar_empleado(empleado_id, current)

@router.delete("/{empleado_id}")
def eliminar_empleado(
    empleado_id: int, 
    service: EmpleadoService = Depends(get_empleado_service)
):
    """
    Desactiva a un empleado (Eliminación lógica). 
    Cambia su estado a 'activo=False' en la base de datos.
    """
    if not service.eliminar_empleado(empleado_id):
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return {"message": "Empleado desactivado (eliminación lógica) correctamente"}
