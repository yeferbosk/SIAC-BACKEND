from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ClienteBase(BaseModel):
    """
    Esquema base para la entidad Cliente con los campos comunes.
    """
    nombre: str
    empresa: Optional[str] = None
    email: EmailStr
    telefono: str
    tipo_cliente: str # 'corporativo', 'individual', 'gobierno'

class ClienteCreate(ClienteBase):
    """
    Esquema para la creación de un nuevo cliente.
    """
    pass

class ClienteUpdate(BaseModel):
    """
    Esquema para la actualización de un cliente existente.
    Permite modificar todos los campos excepto tipo_cliente y fecha_registro.
    """
    nombre: Optional[str] = None
    empresa: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None

class ClienteSchema(ClienteBase):
    """
    Esquema completo para representar un cliente en las respuestas de la API.
    """
    id_cliente: int
    fecha_registro: datetime

    class Config:
        from_attributes = True
