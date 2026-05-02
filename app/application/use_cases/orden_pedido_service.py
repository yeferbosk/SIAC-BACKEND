from typing import List, Optional
from app.domain.entities.orden_pedido import OrdenPedido
from app.domain.ports.orden_pedido_repository import OrdenPedidoRepository

class OrdenPedidoService:
    def __init__(self, repository: OrdenPedidoRepository):
        self.repository = repository

    def crear_orden(self, orden: OrdenPedido) -> OrdenPedido:
        return self.repository.save(orden)

    def obtener_orden(self, orden_id: int) -> Optional[OrdenPedido]:
        return self.repository.get_by_id(orden_id)

    def listar_ordenes(self) -> List[OrdenPedido]:
        return self.repository.get_all()

    def actualizar_orden(self, orden_id: int, orden: OrdenPedido) -> Optional[OrdenPedido]:
        return self.repository.update(orden_id, orden)
