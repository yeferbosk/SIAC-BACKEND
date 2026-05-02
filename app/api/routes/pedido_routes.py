from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.application.use_cases.pedido_service import PedidoService
from app.api.dependencies.services import get_pedido_service
from app.api.schemas.pedido_schema import PedidoSchema, PedidoCreate
from app.domain.entities.pedido import Pedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoSchema)
def crear_pedido(p: PedidoCreate, service: PedidoService = Depends(get_pedido_service)):
    p_domain = Pedido(
        id_pedido=None,
        id_cliente=p.id_cliente,
        id_empleado=p.id_empleado,
        id_transformador=p.id_transformador,
        tipo_pedido=p.tipo_pedido,
        estado=p.estado,
        estado_pago=p.estado_pago,
        monto_total=p.monto_total,
        fecha_hora_visita=p.fecha_hora_visita,
        observaciones=p.observaciones,
        fecha_entrega_estimada=p.fecha_entrega_estimada,
        fecha_entrega_real=p.fecha_entrega_real
    )
    return service.crear_pedido(p_domain)

@router.get("/", response_model=List[PedidoSchema])
def listar_pedidos(service: PedidoService = Depends(get_pedido_service)):
    return service.listar_pedidos()

@router.get("/{pedido_id}", response_model=PedidoSchema)
def obtener_pedido(pedido_id: int, service: PedidoService = Depends(get_pedido_service)):
    p = service.obtener_pedido(pedido_id)
    if not p:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return p
