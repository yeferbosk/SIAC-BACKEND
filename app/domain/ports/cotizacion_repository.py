from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.cotizacion import Cotizacion

class CotizacionRepository(ABC):
    @abstractmethod
    def save(self, cotizacion: Cotizacion) -> Cotizacion:
        pass

    @abstractmethod
    def get_by_id(self, cotizacion_id: int) -> Optional[Cotizacion]:
        pass

    @abstractmethod
    def get_all(self) -> List[Cotizacion]:
        pass

    @abstractmethod
    def update(self, cotizacion_id: int, cotizacion: Cotizacion) -> Optional[Cotizacion]:
        pass
