from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class InteraccionChatbot:
    id_interaccion: Optional[int]
    id_pedido: int
    id_cliente: int
    canal: str # 'whatsapp', 'web', 'email'
    mensaje_usuario: str
    respuesta_bot: str
    fecha_interaccion: Optional[datetime] = None
