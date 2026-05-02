from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.movimiento_inventario import MovimientoInventario
from app.domain.ports.movimiento_inventario_repository import MovimientoInventarioRepository
from app.infrastructure.db.models import MovimientoInventarioModel

class MovimientoInventarioRepositoryImpl(MovimientoInventarioRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, movimiento: MovimientoInventario) -> MovimientoInventario:
        db_m = MovimientoInventarioModel(
            id_transformador=movimiento.id_transformador,
            id_pedido=movimiento.id_pedido,
            id_empleado=movimiento.id_empleado,
            tipo_movimiento=movimiento.tipo_movimiento,
            cantidad=movimiento.cantidad,
            observaciones=movimiento.observaciones
        )
        self.db.add(db_m)
        self.db.commit()
        self.db.refresh(db_m)
        return self._to_domain(db_m)

    def get_by_id(self, movimiento_id: int) -> Optional[MovimientoInventario]:
        db_m = self.db.query(MovimientoInventarioModel).filter(MovimientoInventarioModel.id_movimiento == movimiento_id).first()
        return self._to_domain(db_m) if db_m else None

    def get_all(self) -> List[MovimientoInventario]:
        ms = self.db.query(MovimientoInventarioModel).all()
        return [self._to_domain(m) for m in ms]

    def _to_domain(self, model: MovimientoInventarioModel) -> MovimientoInventario:
        return MovimientoInventario(
            id_movimiento=model.id_movimiento,
            id_transformador=model.id_transformador,
            id_pedido=model.id_pedido,
            id_empleado=model.id_empleado,
            tipo_movimiento=model.tipo_movimiento,
            cantidad=model.cantidad,
            fecha_movimiento=model.fecha_movimiento,
            observaciones=model.observaciones
        )
