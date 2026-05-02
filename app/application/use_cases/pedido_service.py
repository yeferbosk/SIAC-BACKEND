from typing import List, Optional
from app.domain.entities.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepository

class PedidoService:
    def __init__(self, repository: PedidoRepository):
        self.repository = repository

    def crear_pedido(self, pedido: Pedido) -> Pedido:
        return self.repository.save(pedido)

    def obtener_pedido(self, pedido_id: int) -> Optional[Pedido]:
        return self.repository.get_by_id(pedido_id)

    def listar_pedidos(self) -> List[Pedido]:
        return self.repository.get_all()

    def actualizar_pedido(self, pedido_id: int, pedido: Pedido) -> Optional[Pedido]:
        return self.repository.update(pedido_id, pedido)

    def eliminar_pedido(self, pedido_id: int) -> bool:
        return self.repository.delete(pedido_id)
