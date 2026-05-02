from pydantic import BaseModel, EmailStr
from typing import Optional

class EmpleadoBase(BaseModel):
    """
    Esquema base para la entidad Empleado.
    """
    nombre: str
    email: EmailStr
    rol: str # 'administrativo', 'tecnico', 'gerente', 'chatbot'
    area: str # 'atencion_cliente', 'administrativa', 'tecnica', 'gerencia'
    activo: bool = True

class EmpleadoCreate(EmpleadoBase):
    """
    Esquema para la creación de un empleado.
    """
    password: str

class EmpleadoUpdate(BaseModel):
    """
    Esquema para la actualización de un empleado.
    Permite modificar todos los campos principales.
    """
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    area: Optional[str] = None
    activo: Optional[bool] = None

class EmpleadoSchema(EmpleadoBase):
    """
    Esquema completo del empleado para respuestas de la API.
    """
    id_empleado: int

    class Config:
        from_attributes = True
