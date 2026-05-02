from sqlalchemy.orm import Session
from fastapi import Depends
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.repositories.cliente_repository_impl import ClienteRepositoryImpl
from app.application.use_cases.cliente_service import ClienteService
from app.infrastructure.repositories.empleado_repository_impl import EmpleadoRepositoryImpl
from app.application.use_cases.empleado_service import EmpleadoService
from app.infrastructure.repositories.transformador_repository_impl import TransformadorRepositoryImpl
from app.application.use_cases.transformador_service import TransformadorService
from app.infrastructure.repositories.pedido_repository_impl import PedidoRepositoryImpl
from app.application.use_cases.pedido_service import PedidoService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_cliente_service(db: Session = Depends(get_db)):
    repository = ClienteRepositoryImpl(db)
    return ClienteService(repository)

def get_empleado_service(db: Session = Depends(get_db)):
    repository = EmpleadoRepositoryImpl(db)
    return EmpleadoService(repository)

def get_transformador_service(db: Session = Depends(get_db)):
    repository = TransformadorRepositoryImpl(db)
    return TransformadorService(repository)

def get_pedido_service(db: Session = Depends(get_db)):
    repository = PedidoRepositoryImpl(db)
    return PedidoService(repository)