from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class TransformadorBase(BaseModel):
    """
    Esquema base para la entidad Transformador.
    """
    referencia: str
    tipo: str # 'monofasico', 'trifasico', 'autotransformador'
    potencia_kva: Decimal
    tension_primaria: Decimal
    tension_secundaria: Decimal
    material_bobinado: str # 'cobre', 'aluminio'
    estado: str = 'disponible' # 'disponible', 'alquilado', 'mantenimiento', 'vendido'
    stock_disponible: int = 0
    precio_venta: Decimal
    precio_alquiler_dia: Decimal

class TransformadorCreate(TransformadorBase):
    """
    Esquema para la creación de un transformador.
    """
    pass

class TransformadorUpdate(BaseModel):
    """
    Esquema para la actualización de un transformador.
    Permite modificar todos los atributos técnicos y comerciales.
    """
    referencia: Optional[str] = None
    tipo: Optional[str] = None
    potencia_kva: Optional[Decimal] = None
    tension_primaria: Optional[Decimal] = None
    tension_secundaria: Optional[Decimal] = None
    material_bobinado: Optional[str] = None
    estado: Optional[str] = None
    stock_disponible: Optional[int] = None
    precio_venta: Optional[Decimal] = None
    precio_alquiler_dia: Optional[Decimal] = None

class TransformadorSchema(TransformadorBase):
    """
    Esquema completo del transformador para respuestas de la API.
    """
    id_transformador: int

    class Config:
        from_attributes = True
