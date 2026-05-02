from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class Pedido:
    id_pedido: Optional[int]
    id_cliente: int
    id_empleado: int
    id_transformador: int
    tipo_pedido: str # 'compra', 'alquiler', 'mantenimiento', 'reparacion'
    estado: str # 'en_proceso', 'completado', 'cancelado'
    estado_pago: str # 'no_pagado', 'seña_pagada', 'pagado'
    monto_total: Decimal
    fecha_hora_visita: Optional[datetime] = None
    observaciones: Optional[str] = None
    fecha_pedido: Optional[datetime] = None
    fecha_entrega_estimada: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None
    updated_at: Optional[datetime] = None