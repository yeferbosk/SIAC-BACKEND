from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Cliente:
    id_cliente: Optional[int]
    nombre: str
    empresa: Optional[str]
    email: str
    telefono: str
    tipo_cliente: str
    fecha_registro: Optional[datetime] = None