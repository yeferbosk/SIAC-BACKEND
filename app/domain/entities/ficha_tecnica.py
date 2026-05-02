from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class FichaTecnica:
    id_ficha: Optional[int]
    id_pedido: int
    id_transformador: int
    especificaciones: str
    normas_aplicables: str
    condiciones_instalacion: Optional[str] = None
    fecha_generacion: Optional[datetime] = None
