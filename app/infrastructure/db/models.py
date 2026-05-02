from sqlalchemy import Column, Integer, String, Enum, TIMESTAMP, Numeric, Boolean, ForeignKey, Text, DateTime
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.infrastructure.db.base import Base


class ClienteModel(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    empresa = Column(String(150))
    email = Column(String(180), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    tipo_cliente = Column(Enum('corporativo', 'individual', 'gobierno'), nullable=False)
    fecha_registro = Column(TIMESTAMP, server_default=func.now())

    pedidos = relationship("PedidoModel", back_populates="cliente")
    interacciones = relationship("InteraccionChatbotModel", back_populates="cliente")


class EmpleadoModel(Base):
    __tablename__ = "empleado"

    id_empleado = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    email = Column(String(180), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(Enum('administrativo', 'tecnico', 'gerente', 'chatbot'), nullable=False)
    area = Column(Enum('atencion_cliente', 'administrativa', 'tecnica', 'gerencia'), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    pedidos = relationship("PedidoModel", back_populates="empleado")
    cotizaciones = relationship("CotizacionModel", back_populates="empleado")
    movimientos = relationship("MovimientoInventarioModel", back_populates="empleado")
    registros_financieros = relationship("RegistroFinancieroModel", back_populates="empleado")


class TransformadorModel(Base):
    __tablename__ = "transformador"

    id_transformador = Column(Integer, primary_key=True, index=True)
    referencia = Column(String(80), unique=True, nullable=False)
    tipo = Column(Enum('monofasico', 'trifasico', 'autotransformador'), nullable=False)
    potencia_kva = Column(Numeric(10, 2), nullable=False)
    tension_primaria = Column(Numeric(10, 2), nullable=False)
    tension_secundaria = Column(Numeric(10, 2), nullable=False)
    material_bobinado = Column(Enum('cobre', 'aluminio'), nullable=False)
    estado = Column(Enum('disponible', 'alquilado', 'mantenimiento', 'vendido'), default='disponible', nullable=False)
    stock_disponible = Column(Integer, default=0, nullable=False)
    precio_venta = Column(Numeric(14, 2), nullable=False)
    precio_alquiler_dia = Column(Numeric(14, 2), nullable=False)

    pedidos = relationship("PedidoModel", back_populates="transformador")
    fichas_tecnicas = relationship("FichaTecnicaModel", back_populates="transformador")
    movimientos = relationship("MovimientoInventarioModel", back_populates="transformador")


class PedidoModel(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=False)
    id_transformador = Column(Integer, ForeignKey("transformador.id_transformador"), nullable=False)

    tipo_pedido = Column(Enum('compra', 'alquiler', 'mantenimiento', 'reparacion'), nullable=False)
    estado = Column(Enum('en_proceso', 'completado', 'cancelado'), default='en_proceso', nullable=False)
    estado_pago = Column(Enum('no_pagado', 'seña_pagada', 'pagado'), default='no_pagado', nullable=False)

    fecha_hora_visita = Column(DateTime)
    observaciones = Column(Text)
    monto_total = Column(Numeric(14, 2), nullable=False)
    fecha_pedido = Column(TIMESTAMP, server_default=func.now())
    fecha_entrega_estimada = Column(DateTime)
    fecha_entrega_real = Column(DateTime)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    cliente = relationship("ClienteModel", back_populates="pedidos")
    empleado = relationship("EmpleadoModel", back_populates="pedidos")
    transformador = relationship("TransformadorModel", back_populates="pedidos")
    interacciones = relationship("InteraccionChatbotModel", back_populates="pedido")
    cotizacion = relationship("CotizacionModel", back_populates="pedido", uselist=False)
    ficha_tecnica = relationship("FichaTecnicaModel", back_populates="pedido", uselist=False)
    orden = relationship("OrdenPedidoModel", back_populates="pedido", uselist=False)
    movimientos = relationship("MovimientoInventarioModel", back_populates="pedido")
    registros_financieros = relationship("RegistroFinancieroModel", back_populates="pedido")


class InteraccionChatbotModel(Base):
    __tablename__ = "interaccion_chatbot"

    id_interaccion = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)
    canal = Column(Enum('whatsapp', 'web', 'email'), nullable=False)
    mensaje_usuario = Column(Text, nullable=False)
    respuesta_bot = Column(Text, nullable=False)
    fecha_interaccion = Column(TIMESTAMP, server_default=func.now())

    pedido = relationship("PedidoModel", back_populates="interacciones")
    cliente = relationship("ClienteModel", back_populates="interacciones")


class CotizacionModel(Base):
    __tablename__ = "cotizacion"

    id_cotizacion = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), unique=True, nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=False)
    numero_cotizacion = Column(String(40), unique=True, nullable=False)
    subtotal = Column(Numeric(14, 2), nullable=False)
    iva = Column(Numeric(14, 2), default=0, nullable=False)
    total = Column(Numeric(14, 2), nullable=False)
    estado = Column(Enum('borrador', 'enviada', 'aceptada', 'rechazada', 'vencida'), default='borrador', nullable=False)
    fecha_emision = Column(TIMESTAMP, server_default=func.now())
    fecha_vencimiento = Column(DateTime, nullable=False)

    pedido = relationship("PedidoModel", back_populates="cotizacion")
    empleado = relationship("EmpleadoModel", back_populates="cotizaciones")
    orden = relationship("OrdenPedidoModel", back_populates="cotizacion", uselist=False)


class FichaTecnicaModel(Base):
    __tablename__ = "ficha_tecnica"

    id_ficha = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)
    id_transformador = Column(Integer, ForeignKey("transformador.id_transformador"), nullable=False)
    especificaciones = Column(Text, nullable=False)
    normas_aplicables = Column(String(255), nullable=False)
    condiciones_instalacion = Column(Text)
    fecha_generacion = Column(TIMESTAMP, server_default=func.now())

    pedido = relationship("PedidoModel", back_populates="ficha_tecnica")
    transformador = relationship("TransformadorModel", back_populates="fichas_tecnicas")


class OrdenPedidoModel(Base):
    __tablename__ = "orden_pedido"

    id_orden = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), unique=True, nullable=False)
    id_cotizacion = Column(Integer, ForeignKey("cotizacion.id_cotizacion"), unique=True, nullable=False)
    numero_orden = Column(String(40), unique=True, nullable=False)
    metodo_pago = Column(Enum('transferencia', 'efectivo', 'cheque', 'credito'), nullable=False)
    id_transferencia = Column(String(120))
    monto_pagado = Column(Numeric(14, 2), nullable=False)
    estado = Column(Enum('pendiente', 'confirmado', 'anulado'), default='pendiente', nullable=False)
    fecha_confirmacion = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    pedido = relationship("PedidoModel", back_populates="orden")
    cotizacion = relationship("CotizacionModel", back_populates="orden")


class MovimientoInventarioModel(Base):
    __tablename__ = "movimiento_inventario"

    id_movimiento = Column(Integer, primary_key=True, index=True)
    id_transformador = Column(Integer, ForeignKey("transformador.id_transformador"), nullable=False)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"))
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=False)
    tipo_movimiento = Column(Enum('entrada', 'salida_venta', 'salida_alquiler', 'devolucion_alquiler', 'ajuste_inventario'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    fecha_movimiento = Column(TIMESTAMP, server_default=func.now())
    observaciones = Column(Text)

    transformador = relationship("TransformadorModel", back_populates="movimientos")
    pedido = relationship("PedidoModel", back_populates="movimientos")
    empleado = relationship("EmpleadoModel", back_populates="movimientos")


class RegistroFinancieroModel(Base):
    __tablename__ = "registro_financiero"

    id_registro = Column(Integer, primary_key=True, index=True)
    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido"), nullable=False)
    id_empleado = Column(Integer, ForeignKey("empleado.id_empleado"), nullable=False)
    monto = Column(Numeric(14, 2), nullable=False)
    tipo_transaccion = Column(Enum('ingreso_venta', 'ingreso_alquiler', 'ingreso_mantenimiento', 'egreso_proveedor', 'egreso_devolucion'), nullable=False)
    metodo_pago = Column(Enum('transferencia', 'efectivo', 'cheque', 'credito'), nullable=False)
    estado_pago = Column(Enum('pendiente', 'completado', 'fallido', 'reembolsado'), default='pendiente', nullable=False)
    fecha_transaccion = Column(TIMESTAMP, server_default=func.now())
    comprobante = Column(String(180))

    pedido = relationship("PedidoModel", back_populates="registros_financieros")
    empleado = relationship("EmpleadoModel", back_populates="registros_financieros")

class AuditoriaLogModel(Base):
    __tablename__ = 'auditoria_log'
    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_empleado = Column(Integer, ForeignKey('empleado.id_empleado'), nullable=True)
    accion = Column(Enum('INSERT', 'UPDATE', 'DELETE'), nullable=False)
    tabla_nombre = Column(String(50), nullable=False)
    registro_id = Column(Integer, nullable=False)
    detalle = Column(Text, nullable=True)
    fecha = Column(DateTime, default=datetime.utcnow)

    # Relación
    empleado = relationship("EmpleadoModel")