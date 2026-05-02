from typing import List, Optional
from app.domain.entities.transformador import Transformador
from app.domain.ports.transformador_repository import TransformadorRepository

class TransformadorService:
    """
    Servicio para el control de inventario técnico y comercial de transformadores.
    """

    def __init__(self, repository: TransformadorRepository):
        """
        Inyecta el repositorio de transformadores.
        """
        self.repository = repository

    def crear_transformador(self, transformador: Transformador) -> Transformador:
        """
        Registra un transformador en el inventario.
        """
        return self.repository.save(transformador)

    def obtener_transformador(self, transformador_id: int) -> Optional[Transformador]:
        """
        Busca las especificaciones de un transformador por su ID.
        """
        return self.repository.get_by_id(transformador_id)

    def listar_transformadores(self) -> List[Transformador]:
        """
        Obtiene la lista de todos los transformadores en el catálogo.
        """
        return self.repository.get_all()

    def actualizar_transformador(self, transformador_id: int, transformador: Transformador) -> Optional[Transformador]:
        """
        Actualiza cualquier información técnica o de precio de un transformador.
        """
        return self.repository.update(transformador_id, transformador)

    def eliminar_transformador(self, transformador_id: int) -> bool:
        """
        Elimina un registro de transformador del sistema.
        """
        return self.repository.delete(transformador_id)
