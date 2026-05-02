from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.empleado import Empleado

class EmpleadoRepository(ABC):
    @abstractmethod
    def save(self, empleado: Empleado) -> Empleado:
        pass

    @abstractmethod
    def get_by_id(self, empleado_id: int) -> Optional[Empleado]:
        pass

    @abstractmethod
    def get_all(self) -> List[Empleado]:
        pass

    @abstractmethod
    def update(self, empleado_id: int, empleado: Empleado) -> Optional[Empleado]:
        pass

    @abstractmethod
    def delete(self, empleado_id: int) -> bool:
        pass
