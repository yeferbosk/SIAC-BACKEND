from typing import List, Optional
from app.domain.entities.empleado import Empleado
from app.domain.ports.empleado_repository import EmpleadoRepository

class EmpleadoService:
    """
    Servicio encargado de la gestión de empleados en el SIAC.
    """

    def __init__(self, repository: EmpleadoRepository):
        """
        Inyecta la implementación del repositorio de empleados.
        """
        self.repository = repository

    def crear_empleado(self, empleado: Empleado) -> Empleado:
        """
        Registra un nuevo colaborador.
        """
        return self.repository.save(empleado)

    def obtener_empleado(self, empleado_id: int) -> Optional[Empleado]:
        """
        Busca un empleado por su ID único.
        """
        return self.repository.get_by_id(empleado_id)

    def listar_empleados(self) -> List[Empleado]:
        """
        Lista todos los empleados registrados en el sistema.
        """
        return self.repository.get_all()

    def actualizar_empleado(self, empleado_id: int, empleado: Empleado) -> Optional[Empleado]:
        """
        Actualiza los datos (nombre, email, rol, area, activo) de un empleado.
        """
        return self.repository.update(empleado_id, empleado)

    def eliminar_empleado(self, empleado_id: int) -> bool:
        """
        Realiza la eliminación lógica (desactivación) de un empleado.
        """
        return self.repository.delete(empleado_id)
