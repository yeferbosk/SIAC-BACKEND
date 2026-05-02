from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.ficha_tecnica import FichaTecnica

class FichaTecnicaRepository(ABC):
    @abstractmethod
    def save(self, ficha: FichaTecnica) -> FichaTecnica:
        pass

    @abstractmethod
    def get_by_id(self, ficha_id: int) -> Optional[FichaTecnica]:
        pass

    @abstractmethod
    def get_all(self) -> List[FichaTecnica]:
        pass
