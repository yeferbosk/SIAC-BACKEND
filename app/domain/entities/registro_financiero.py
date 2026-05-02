from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from decimal import Decimal

@dataclass
class RegistroFinanciero:
    id_registro: Optional[int]
    id_pedido: int
    id_empleado: int
    monto: Decimal
    tipo_transaccion: str # 'ingreso_venta', 'ingreso_alquiler', 'ingreso_mantenimiento', 'egreso_proveedor', 'egreso_devolucion'
    metodo_pago: str # 'transferencia', 'efectivo', 'cheque', 'credito'
    estado_pago: str = 'pendiente' # 'pendiente', 'completado', 'fallido', 'reembolsado'
    fecha_transaccion: Optional[datetime] = None
    comprobante: Optional[str] = None
