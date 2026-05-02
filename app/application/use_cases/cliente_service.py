from typing import List, Optional
from app.domain.entities.cliente import Cliente
from app.domain.ports.cliente_repository import ClienteRepository


class ClienteService:
    """
    Servicio de aplicación para gestionar la lógica de negocio de los Clientes.
    Actúa como puente entre los controladores (API) y el repositorio (Persistencia).
    """

    def __init__(self, repository: ClienteRepository):
        """
        Inyecta el repositorio necesario para las operaciones de persistencia.
        """
        self.repository = repository

    def crear_cliente(self, cliente: Cliente) -> Cliente:
        """
        Lógica para registrar un nuevo cliente.
        """
        return self.repository.save(cliente)

    def obtener_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca un cliente por su identificador primario.
        """
        return self.repository.get_by_id(cliente_id)

    def obtener_por_email(self, email: str) -> Optional[Cliente]:
        """
        Busca un cliente por su dirección de correo electrónico.
        """
        return self.repository.get_by_email(email)

    def listar_clientes(self) -> List[Cliente]:
        """
        Obtiene el catálogo completo de clientes registrados.
        """
        return self.repository.get_all()

    def actualizar_cliente(
        self, cliente_id: int, cliente: Cliente
    ) -> Optional[Cliente]:
        """
        Lógica para actualizar la información de un cliente existente.
        """
        return self.repository.update(cliente_id, cliente)

    def eliminar_cliente(self, cliente_id: int) -> bool:
        """
        Elimina el registro de un cliente del sistema.
        """
        return self.repository.delete(cliente_id)