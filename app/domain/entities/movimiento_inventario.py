from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class MovimientoInventario:
    id_movimiento: Optional[int]
    id_transformador: int
    id_empleado: int
    tipo_movimiento: str # 'entrada', 'salida_venta', 'salida_alquiler', 'devolucion_alquiler', 'ajuste_inventario'
    cantidad: int
    id_pedido: Optional[int] = None
    fecha_movimiento: Optional[datetime] = None
    observaciones: Optional[str] = None
