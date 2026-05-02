from typing import List, Optional
from app.domain.entities.registro_financiero import RegistroFinanciero
from app.domain.ports.registro_financiero_repository import RegistroFinancieroRepository

class RegistroFinancieroService:
    def __init__(self, repository: RegistroFinancieroRepository):
        self.repository = repository

    def crear_registro(self, registro: RegistroFinanciero) -> RegistroFinanciero:
        return self.repository.save(registro)

    def obtener_registro(self, registro_id: int) -> Optional[RegistroFinanciero]:
        return self.repository.get_by_id(registro_id)

    def listar_registros(self) -> List[RegistroFinanciero]:
        return self.repository.get_all()
