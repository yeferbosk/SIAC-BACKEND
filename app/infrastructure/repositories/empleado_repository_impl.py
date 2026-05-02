from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.empleado import Empleado
from app.domain.ports.empleado_repository import EmpleadoRepository
from app.infrastructure.db.models import EmpleadoModel

class EmpleadoRepositoryImpl(EmpleadoRepository):
    """
    Implementación del repositorio de Empleados.
    Incluye lógica para eliminación lógica (cambiar estado a inactivo).
    """

    def __init__(self, db: Session):
        """
        Inicializa con la sesión de base de datos.
        """
        self.db = db

    def save(self, empleado: Empleado) -> Empleado:
        """
        Registra un nuevo empleado.
        """
        # 1. Crear el modelo con los datos iniciales
        db_empleado = EmpleadoModel(
            nombre=empleado.nombre,
            email=empleado.email,
            rol=empleado.rol,
            area=empleado.area,
            activo=empleado.activo
        )
        # 2. Persistir en la base de datos
        self.db.add(db_empleado)
        self.db.commit()
        self.db.refresh(db_empleado)
        return self._to_domain(db_empleado)

    def get_by_id(self, empleado_id: int) -> Optional[Empleado]:
        """
        Busca un empleado por su ID.
        """
        db_emp = self.db.query(EmpleadoModel).filter(EmpleadoModel.id_empleado == empleado_id).first()
        return self._to_domain(db_emp) if db_emp else None

    def get_all(self) -> List[Empleado]:
        """
        Obtiene todos los empleados (activos e inactivos).
        """
        emps = self.db.query(EmpleadoModel).all()
        return [self._to_domain(e) for e in emps]

    def update(self, empleado_id: int, empleado: Empleado) -> Optional[Empleado]:
        """
        Actualiza la información de un empleado.
        """
        # 1. Localizar el registro
        db_emp = self.db.query(EmpleadoModel).filter(EmpleadoModel.id_empleado == empleado_id).first()
        if not db_emp:
            return None
        
        # 2. Aplicar los cambios
        db_emp.nombre = empleado.nombre
        db_emp.email = empleado.email
        db_emp.rol = empleado.rol
        db_emp.area = empleado.area
        db_emp.activo = empleado.activo # Permite reactivar o desactivar desde aquí también
        
        # 3. Confirmar cambios
        self.db.commit()
        self.db.refresh(db_emp)
        return self._to_domain(db_emp)

    def delete(self, empleado_id: int) -> bool:
        """
        Realiza una eliminación LÓGICA del empleado.
        Cambia el atributo 'activo' a False.
        """
        # 1. Buscar el empleado
        db_emp = self.db.query(EmpleadoModel).filter(EmpleadoModel.id_empleado == empleado_id).first()
        if not db_emp:
            return False
        
        # 2. Cambiar estado a inactivo en lugar de borrar el registro
        db_emp.activo = False
        
        # 3. Confirmar en la DB
        self.db.commit()
        return True

    def _to_domain(self, model: EmpleadoModel) -> Empleado:
        """
        Conversión de modelo SQLAlchemy a entidad de Dominio.
        """
        return Empleado(
            id_empleado=model.id_empleado,
            nombre=model.nombre,
            email=model.email,
            rol=model.rol,
            area=model.area,
            activo=model.activo
        )
