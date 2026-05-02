from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.registro_financiero import RegistroFinanciero

class RegistroFinancieroRepository(ABC):
    @abstractmethod
    def save(self, registro: RegistroFinanciero) -> RegistroFinanciero:
        pass

    @abstractmethod
    def get_by_id(self, registro_id: int) -> Optional[RegistroFinanciero]:
        pass

    @abstractmethod
    def get_all(self) -> List[RegistroFinanciero]:
        pass
