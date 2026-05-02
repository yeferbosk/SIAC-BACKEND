from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.cliente import Cliente


class ClienteRepository(ABC):

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Cliente]:
        pass

    @abstractmethod
    def get_all(self) -> List[Cliente]:
        pass

    @abstractmethod
    def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> bool:
        pass