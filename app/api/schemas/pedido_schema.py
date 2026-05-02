from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PedidoBase(BaseModel):
    id_cliente: int
    id_empleado: int
    id_transformador: int
    tipo_pedido: str
    estado: str = 'en_proceso'
    estado_pago: str = 'no_pagado'
    fecha_hora_visita: Optional[datetime] = None
    observaciones: Optional[str] = None
    monto_total: Decimal
    fecha_entrega_estimada: Optional[datetime] = None
    fecha_entrega_real: Optional[datetime] = None

class PedidoCreate(PedidoBase):
    pass

class PedidoSchema(PedidoBase):
    id_pedido: int
    fecha_pedido: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
