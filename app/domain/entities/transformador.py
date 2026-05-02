from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class Transformador:
    id_transformador: Optional[int]
    referencia: str
    tipo: str # 'monofasico', 'trifasico', 'autotransformador'
    potencia_kva: Decimal
    tension_primaria: Decimal
    tension_secundaria: Decimal
    material_bobinado: str # 'cobre', 'aluminio'
    estado: str # 'disponible', 'alquilado', 'mantenimiento', 'vendido'
    stock_disponible: int
    precio_venta: Decimal
    precio_alquiler_dia: Decimal
