from sqlalchemy.orm import Session
from typing import List, Optional

from app.domain.entities.cliente import Cliente
from app.domain.ports.cliente_repository import ClienteRepository
from app.infrastructure.db.models import ClienteModel


class ClienteRepositoryImpl(ClienteRepository):
    """
    Implementación del repositorio de Clientes utilizando SQLAlchemy.
    Maneja la persistencia de datos en la base de datos MySQL.
    """

    def __init__(self, db: Session):
        """
        Inicializa el repositorio con una sesión de base de datos.
        """
        self.db = db

    def save(self, cliente: Cliente) -> Cliente:
        """
        Guarda un nuevo cliente en la base de datos.
        """
        # 1. Crear la instancia del modelo de base de datos
        db_cliente = ClienteModel(
            nombre=cliente.nombre,
            empresa=cliente.empresa,
            email=cliente.email,
            telefono=cliente.telefono,
            tipo_cliente=cliente.tipo_cliente,
        )
        # 2. Agregar y confirmar la transacción
        self.db.add(db_cliente)
        self.db.commit()
        # 3. Refrescar para obtener el ID generado
        self.db.refresh(db_cliente)
        # 4. Retornar la entidad de dominio
        return self._to_domain(db_cliente)

    def get_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """
        Busca un cliente por su ID único.
        """
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == cliente_id).first()
        return self._to_domain(db_cliente) if db_cliente else None

    def get_by_email(self, email: str) -> Optional[Cliente]:
        """
        Busca un cliente por su correo electrónico.
        """
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.email == email).first()
        return self._to_domain(db_cliente) if db_cliente else None

    def get_all(self) -> List[Cliente]:
        """
        Obtiene la lista de todos los clientes registrados.
        """
        clientes = self.db.query(ClienteModel).all()
        return [self._to_domain(c) for c in clientes]

    def update(self, cliente_id: int, cliente: Cliente) -> Optional[Cliente]:
        """
        Actualiza los datos de un cliente existente.
        Permite modificar nombre, empresa, email y teléfono.
        """
        # 1. Buscar el registro existente
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == cliente_id).first()
        if not db_cliente:
            return None
        
        # 2. Actualizar los campos permitidos
        db_cliente.nombre = cliente.nombre
        db_cliente.empresa = cliente.empresa
        db_cliente.email = cliente.email
        db_cliente.telefono = cliente.telefono
        # Nota: tipo_cliente y fecha_registro no se modifican según requerimiento

        # 3. Guardar cambios
        self.db.commit()
        self.db.refresh(db_cliente)
        return self._to_domain(db_cliente)

    def delete(self, cliente_id: int) -> bool:
        """
        Elimina físicamente un cliente de la base de datos.
        """
        db_cliente = self.db.query(ClienteModel).filter(ClienteModel.id_cliente == cliente_id).first()
        if not db_cliente:
            return False
        self.db.delete(db_cliente)
        self.db.commit()
        return True

    def _to_domain(self, model: ClienteModel) -> Cliente:
        """
        Mapea un modelo de SQLAlchemy a una entidad de dominio Cliente.
        """
        return Cliente(
            id_cliente=model.id_cliente,
            nombre=model.nombre,
            empresa=model.empresa,
            email=model.email,
            telefono=model.telefono,
            tipo_cliente=model.tipo_cliente,
            fecha_registro=model.fecha_registro,
        )