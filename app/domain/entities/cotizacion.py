from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class Cotizacion:
    id_cotizacion: Optional[int]
    id_pedido: int
    id_empleado: int
    numero_cotizacion: str
    subtotal: Decimal
    iva: Decimal
    total: Decimal
    estado: str # 'borrador', 'enviada', 'aceptada', 'rechazada', 'vencida'
    fecha_vencimiento: datetime
    fecha_emision: Optional[datetime] = None
