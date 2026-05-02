from typing import List, Optional
from app.domain.entities.cotizacion import Cotizacion
from app.domain.ports.cotizacion_repository import CotizacionRepository

class CotizacionService:
    def __init__(self, repository: CotizacionRepository):
        self.repository = repository

    def crear_cotizacion(self, cotizacion: Cotizacion) -> Cotizacion:
        return self.repository.save(cotizacion)

    def obtener_cotizacion(self, cotizacion_id: int) -> Optional[Cotizacion]:
        return self.repository.get_by_id(cotizacion_id)

    def listar_cotizaciones(self) -> List[Cotizacion]:
        return self.repository.get_all()

    def actualizar_cotizacion(self, cotizacion_id: int, cotizacion: Cotizacion) -> Optional[Cotizacion]:
        return self.repository.update(cotizacion_id, cotizacion)
