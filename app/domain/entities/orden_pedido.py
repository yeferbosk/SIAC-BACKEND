from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class OrdenPedido:
    id_orden: Optional[int]
    id_pedido: int
    id_cotizacion: int
    numero_orden: str
    metodo_pago: str # 'transferencia', 'efectivo', 'cheque', 'credito'
    monto_pagado: Decimal
    id_transferencia: Optional[str] = None
    estado: str = 'pendiente' # 'pendiente', 'confirmado', 'anulado'
    fecha_confirmacion: Optional[datetime] = None
    updated_at: Optional[datetime] = None
