from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.pedido import Pedido
from app.domain.ports.pedido_repository import PedidoRepository
from app.infrastructure.db.models import PedidoModel

class PedidoRepositoryImpl(PedidoRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, pedido: Pedido) -> Pedido:
        db_p = PedidoModel(
            id_cliente=pedido.id_cliente,
            id_empleado=pedido.id_empleado,
            id_transformador=pedido.id_transformador,
            tipo_pedido=pedido.tipo_pedido,
            estado=pedido.estado,
            estado_pago=pedido.estado_pago,
            fecha_hora_visita=pedido.fecha_hora_visita,
            observaciones=pedido.observaciones,
            monto_total=pedido.monto_total,
            fecha_entrega_estimada=pedido.fecha_entrega_estimada,
            fecha_entrega_real=pedido.fecha_entrega_real
        )
        self.db.add(db_p)
        self.db.commit()
        self.db.refresh(db_p)
        return self._to_domain(db_p)

    def get_by_id(self, pedido_id: int) -> Optional[Pedido]:
        db_p = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()
        return self._to_domain(db_p) if db_p else None

    def get_all(self) -> List[Pedido]:
        ps = self.db.query(PedidoModel).all()
        return [self._to_domain(p) for p in ps]

    def update(self, pedido_id: int, pedido: Pedido) -> Optional[Pedido]:
        db_p = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()
        if not db_p:
            return None
        db_p.id_cliente = pedido.id_cliente
        db_p.id_empleado = pedido.id_empleado
        db_p.id_transformador = pedido.id_transformador
        db_p.tipo_pedido = pedido.tipo_pedido
        db_p.estado = pedido.estado
        db_p.estado_pago = pedido.estado_pago
        db_p.fecha_hora_visita = pedido.fecha_hora_visita
        db_p.observaciones = pedido.observaciones
        db_p.monto_total = pedido.monto_total
        db_p.fecha_entrega_estimada = pedido.fecha_entrega_estimada
        db_p.fecha_entrega_real = pedido.fecha_entrega_real
        self.db.commit()
        self.db.refresh(db_p)
        return self._to_domain(db_p)

    def delete(self, pedido_id: int) -> bool:
        db_p = self.db.query(PedidoModel).filter(PedidoModel.id_pedido == pedido_id).first()
        if not db_p:
            return False
        self.db.delete(db_p)
        self.db.commit()
        return True

    def _to_domain(self, model: PedidoModel) -> Pedido:
        return Pedido(
            id_pedido=model.id_pedido,
            id_cliente=model.id_cliente,
            id_empleado=model.id_empleado,
            id_transformador=model.id_transformador,
            tipo_pedido=model.tipo_pedido,
            estado=model.estado,
            estado_pago=model.estado_pago,
            monto_total=model.monto_total,
            fecha_hora_visita=model.fecha_hora_visita,
            observaciones=model.observaciones,
            fecha_pedido=model.fecha_pedido,
            fecha_entrega_estimada=model.fecha_entrega_estimada,
            fecha_entrega_real=model.fecha_entrega_real,
            updated_at=model.updated_at
        )
