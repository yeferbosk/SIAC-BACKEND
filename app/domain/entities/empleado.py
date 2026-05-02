from dataclasses import dataclass
from typing import Optional

@dataclass
class Empleado:
    id_empleado: Optional[int]
    nombre: str
    email: str
    rol: str # 'administrativo', 'tecnico', 'gerente', 'chatbot'
    area: str # 'atencion_cliente', 'administrativa', 'tecnica', 'gerencia'
    password: Optional[str] = None
    activo: bool = True