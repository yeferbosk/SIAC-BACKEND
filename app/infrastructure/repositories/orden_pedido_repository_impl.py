from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.orden_pedido import OrdenPedido
from app.domain.ports.orden_pedido_repository import OrdenPedidoRepository
from app.infrastructure.db.models import OrdenPedidoModel

class OrdenPedidoRepositoryImpl(OrdenPedidoRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, orden: OrdenPedido) -> OrdenPedido:
        db_o = OrdenPedidoModel(
            id_pedido=orden.id_pedido,
            id_cotizacion=orden.id_cotizacion,
            numero_orden=orden.numero_orden,
            metodo_pago=orden.metodo_pago,
            id_transferencia=orden.id_transferencia,
            monto_pagado=orden.monto_pagado,
            estado=orden.estado
        )
        self.db.add(db_o)
        self.db.commit()
        self.db.refresh(db_o)
        return self._to_domain(db_o)

    def get_by_id(self, orden_id: int) -> Optional[OrdenPedido]:
        db_o = self.db.query(OrdenPedidoModel).filter(OrdenPedidoModel.id_orden == orden_id).first()
        return self._to_domain(db_o) if db_o else None

    def get_all(self) -> List[OrdenPedido]:
        os = self.db.query(OrdenPedidoModel).all()
        return [self._to_domain(o) for o in os]

    def update(self, orden_id: int, orden: OrdenPedido) -> Optional[OrdenPedido]:
        db_o = self.db.query(OrdenPedidoModel).filter(OrdenPedidoModel.id_orden == orden_id).first()
        if not db_o:
            return None
        db_o.estado = orden.estado
        db_o.monto_pagado = orden.monto_pagado
        db_o.metodo_pago = orden.metodo_pago
        db_o.id_transferencia = orden.id_transferencia
        self.db.commit()
        self.db.refresh(db_o)
        return self._to_domain(db_o)

    def _to_domain(self, model: OrdenPedidoModel) -> OrdenPedido:
        return OrdenPedido(
            id_orden=model.id_orden,
            id_pedido=model.id_pedido,
            id_cotizacion=model.id_cotizacion,
            numero_orden=model.numero_orden,
            metodo_pago=model.metodo_pago,
            monto_pagado=model.monto_pagado,
            id_transferencia=model.id_transferencia,
            estado=model.estado,
            fecha_confirmacion=model.fecha_confirmacion,
            updated_at=model.updated_at
        )
