from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.cotizacion import Cotizacion
from app.domain.ports.cotizacion_repository import CotizacionRepository
from app.infrastructure.db.models import CotizacionModel

class CotizacionRepositoryImpl(CotizacionRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, cotizacion: Cotizacion) -> Cotizacion:
        db_c = CotizacionModel(
            id_pedido=cotizacion.id_pedido,
            id_empleado=cotizacion.id_empleado,
            numero_cotizacion=cotizacion.numero_cotizacion,
            subtotal=cotizacion.subtotal,
            iva=cotizacion.iva,
            total=cotizacion.total,
            estado=cotizacion.estado,
            fecha_vencimiento=cotizacion.fecha_vencimiento
        )
        self.db.add(db_c)
        self.db.commit()
        self.db.refresh(db_c)
        return self._to_domain(db_c)

    def get_by_id(self, cotizacion_id: int) -> Optional[Cotizacion]:
        db_c = self.db.query(CotizacionModel).filter(CotizacionModel.id_cotizacion == cotizacion_id).first()
        return self._to_domain(db_c) if db_c else None

    def get_all(self) -> List[Cotizacion]:
        cs = self.db.query(CotizacionModel).all()
        return [self._to_domain(c) for c in cs]

    def update(self, cotizacion_id: int, cotizacion: Cotizacion) -> Optional[Cotizacion]:
        db_c = self.db.query(CotizacionModel).filter(CotizacionModel.id_cotizacion == cotizacion_id).first()
        if not db_c:
            return None
        db_c.estado = cotizacion.estado
        db_c.subtotal = cotizacion.subtotal
        db_c.iva = cotizacion.iva
        db_c.total = cotizacion.total
        db_c.fecha_vencimiento = cotizacion.fecha_vencimiento
        self.db.commit()
        self.db.refresh(db_c)
        return self._to_domain(db_c)

    def _to_domain(self, model: CotizacionModel) -> Cotizacion:
        return Cotizacion(
            id_cotizacion=model.id_cotizacion,
            id_pedido=model.id_pedido,
            id_empleado=model.id_empleado,
            numero_cotizacion=model.numero_cotizacion,
            subtotal=model.subtotal,
            iva=model.iva,
            total=model.total,
            estado=model.estado,
            fecha_emision=model.fecha_emision,
            fecha_vencimiento=model.fecha_vencimiento
        )
