from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.movimiento_inventario import MovimientoInventario

class MovimientoInventarioRepository(ABC):
    @abstractmethod
    def save(self, movimiento: MovimientoInventario) -> MovimientoInventario:
        pass

    @abstractmethod
    def get_by_id(self, movimiento_id: int) -> Optional[MovimientoInventario]:
        pass

    @abstractmethod
    def get_all(self) -> List[MovimientoInventario]:
        pass
