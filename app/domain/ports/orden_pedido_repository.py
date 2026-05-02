from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.orden_pedido import OrdenPedido

class OrdenPedidoRepository(ABC):
    @abstractmethod
    def save(self, orden: OrdenPedido) -> OrdenPedido:
        pass

    @abstractmethod
    def get_by_id(self, orden_id: int) -> Optional[OrdenPedido]:
        pass

    @abstractmethod
    def get_all(self) -> List[OrdenPedido]:
        pass

    @abstractmethod
    def update(self, orden_id: int, orden: OrdenPedido) -> Optional[OrdenPedido]:
        pass
