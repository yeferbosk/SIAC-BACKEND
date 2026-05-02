from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.entities.registro_financiero import RegistroFinanciero
from app.domain.ports.registro_financiero_repository import RegistroFinancieroRepository
from app.infrastructure.db.models import RegistroFinancieroModel

class RegistroFinancieroRepositoryImpl(RegistroFinancieroRepository):
    def __init__(self, db: Session):
        self.db = db

    def save(self, registro: RegistroFinanciero) -> RegistroFinanciero:
        db_r = RegistroFinancieroModel(
            id_pedido=registro.id_pedido,
            id_empleado=registro.id_empleado,
            monto=registro.monto,
            tipo_transaccion=registro.tipo_transaccion,
            metodo_pago=registro.metodo_pago,
            estado_pago=registro.estado_pago,
            comprobante=registro.comprobante
        )
        self.db.add(db_r)
        self.db.commit()
        self.db.refresh(db_r)
        return self._to_domain(db_r)

    def get_by_id(self, registro_id: int) -> Optional[RegistroFinanciero]:
        db_r = self.db.query(RegistroFinancieroModel).filter(RegistroFinancieroModel.id_registro == registro_id).first()
        return self._to_domain(db_r) if db_r else None

    def get_all(self) -> List[RegistroFinanciero]:
        rs = self.db.query(RegistroFinancieroModel).all()
        return [self._to_domain(r) for r in rs]

    def _to_domain(self, model: RegistroFinancieroModel) -> RegistroFinanciero:
        return RegistroFinanciero(
            id_registro=model.id_registro,
            id_pedido=model.id_pedido,
            id_empleado=model.id_empleado,
            monto=model.monto,
            tipo_transaccion=model.tipo_transaccion,
            metodo_pago=model.metodo_pago,
            estado_pago=model.estado_pago,
            fecha_transaccion=model.fecha_transaccion,
            comprobante=model.comprobante
        )
