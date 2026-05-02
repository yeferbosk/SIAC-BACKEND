from typing import List, Optional
from app.domain.entities.movimiento_inventario import MovimientoInventario
from app.domain.ports.movimiento_inventario_repository import MovimientoInventarioRepository

class MovimientoInventarioService:
    def __init__(self, repository: MovimientoInventarioRepository):
        self.repository = repository

    def crear_movimiento(self, movimiento: MovimientoInventario) -> MovimientoInventario:
        return self.repository.save(movimiento)

    def obtener_movimiento(self, movimiento_id: int) -> Optional[MovimientoInventario]:
        return self.repository.get_by_id(movimiento_id)

    def listar_movimientos(self) -> List[MovimientoInventario]:
        return self.repository.get_all()
