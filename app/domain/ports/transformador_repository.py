from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.transformador import Transformador

class TransformadorRepository(ABC):
    @abstractmethod
    def save(self, transformador: Transformador) -> Transformador:
        pass

    @abstractmethod
    def get_by_id(self, transformador_id: int) -> Optional[Transformador]:
        pass

    @abstractmethod
    def get_all(self) -> List[Transformador]:
        pass

    @abstractmethod
    def update(self, transformador_id: int, transformador: Transformador) -> Optional[Transformador]:
        pass

    @abstractmethod
    def delete(self, transformador_id: int) -> bool:
        pass
