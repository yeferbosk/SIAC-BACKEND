from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.transformador import Transformador
from app.domain.ports.transformador_repository import TransformadorRepository
from app.infrastructure.db.models import TransformadorModel

class TransformadorRepositoryImpl(TransformadorRepository):
    """
    Implementación del repositorio para la gestión técnica de transformadores.
    """

    def __init__(self, db: Session):
        """
        Constructor que recibe la sesión de la base de datos.
        """
        self.db = db

    def save(self, transformador: Transformador) -> Transformador:
        """
        Registra un transformador en el inventario.
        """
        # 1. Crear el objeto del modelo con los parámetros técnicos
        db_t = TransformadorModel(
            referencia=transformador.referencia,
            tipo=transformador.tipo,
            potencia_kva=transformador.potencia_kva,
            tension_primaria=transformador.tension_primaria,
            tension_secundaria=transformador.tension_secundaria,
            material_bobinado=transformador.material_bobinado,
            estado=transformador.estado,
            stock_disponible=transformador.stock_disponible,
            precio_venta=transformador.precio_venta,
            precio_alquiler_dia=transformador.precio_alquiler_dia
        )
        # 2. Agregar y guardar en la base de datos
        self.db.add(db_t)
        self.db.commit()
        self.db.refresh(db_t)
        return self._to_domain(db_t)

    def get_by_id(self, transformador_id: int) -> Optional[Transformador]:
        """
        Busca un transformador específico por su ID.
        """
        db_t = self.db.query(TransformadorModel).filter(TransformadorModel.id_transformador == transformador_id).first()
        return self._to_domain(db_t) if db_t else None

    def get_all(self) -> List[Transformador]:
        """
        Lista todo el catálogo de transformadores.
        """
        ts = self.db.query(TransformadorModel).all()
        return [self._to_domain(t) for t in ts]

    def update(self, transformador_id: int, transformador: Transformador) -> Optional[Transformador]:
        """
        Actualiza todos los campos técnicos y comerciales de un transformador.
        """
        # 1. Buscar el registro actual
        db_t = self.db.query(TransformadorModel).filter(TransformadorModel.id_transformador == transformador_id).first()
        if not db_t:
            return None
        
        # 2. Sobrescribir todos los campos con la nueva información
        db_t.referencia = transformador.referencia
        db_t.tipo = transformador.tipo
        db_t.potencia_kva = transformador.potencia_kva
        db_t.tension_primaria = transformador.tension_primaria
        db_t.tension_secundaria = transformador.tension_secundaria
        db_t.material_bobinado = transformador.material_bobinado
        db_t.estado = transformador.estado
        db_t.stock_disponible = transformador.stock_disponible
        db_t.precio_venta = transformador.precio_venta
        db_t.precio_alquiler_dia = transformador.precio_alquiler_dia
        
        # 3. Guardar cambios en la base de datos
        self.db.commit()
        self.db.refresh(db_t)
        return self._to_domain(db_t)

    def delete(self, transformador_id: int) -> bool:
        """
        Elimina un transformador del sistema.
        """
        db_t = self.db.query(TransformadorModel).filter(TransformadorModel.id_transformador == transformador_id).first()
        if not db_t:
            return False
        self.db.delete(db_t)
        self.db.commit()
        return True

    def _to_domain(self, model: TransformadorModel) -> Transformador:
        """
        Transforma el modelo de persistencia a entidad de dominio.
        """
        return Transformador(
            id_transformador=model.id_transformador,
            referencia=model.referencia,
            tipo=model.tipo,
            potencia_kva=model.potencia_kva,
            tension_primaria=model.tension_primaria,
            tension_secundaria=model.tension_secundaria,
            material_bobinado=model.material_bobinado,
            estado=model.estado,
            stock_disponible=model.stock_disponible,
            precio_venta=model.precio_venta,
            precio_alquiler_dia=model.precio_alquiler_dia
        )
