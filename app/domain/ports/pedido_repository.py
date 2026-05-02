from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.pedido import Pedido

class PedidoRepository(ABC):
    @abstractmethod
    def save(self, pedido: Pedido) -> Pedido:
        pass

    @abstractmethod
    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        pass

    @abstractmethod
    def get_all(self) -> List[Pedido]:
        pass

    @abstractmethod
    def update(self, pedido_id: int, pedido: Pedido) -> Optional[Pedido]:
        pass

    @abstractmethod
    def delete(self, pedido_id: int) -> bool:
        pass
