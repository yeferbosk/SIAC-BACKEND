-- ============================================================
-- SIAC - Sistema Inteligente de Automatización Comercial
-- Transformadores Induelectro
-- Base de datos MySQL - Script COMPLETO CON DATOS DE PRUEBA
-- ============================================================

CREATE DATABASE IF NOT EXISTS siac_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE siac_db;

-- ============================================================
-- MÓDULO 1 - ENTIDADES INDEPENDIENTES (sin FK entrantes)
-- ============================================================

CREATE TABLE cliente (
  id_cliente       INT            NOT NULL AUTO_INCREMENT,
  nombre           VARCHAR(120)   NOT NULL,
  empresa          VARCHAR(150)   NULL,
  email            VARCHAR(180)   NOT NULL,
  telefono         VARCHAR(20)    NOT NULL,
  tipo_cliente     ENUM('corporativo', 'individual', 'gobierno') NOT NULL,
  fecha_registro   TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_cliente PRIMARY KEY (id_cliente),
  CONSTRAINT uq_cliente_email UNIQUE (email)
);

-- ============================================================
CREATE TABLE empleado (
  id_empleado   INT           NOT NULL AUTO_INCREMENT,
  nombre        VARCHAR(120)  NOT NULL,
  email         VARCHAR(180)  NOT NULL,
  password      VARCHAR(255)  NOT NULL, -- Nueva columna para autenticación
  rol           ENUM('administrativo', 'tecnico', 'gerente', 'chatbot') NOT NULL,
  area          ENUM('atencion_cliente', 'administrativa', 'tecnica', 'gerencia') NOT NULL,
  activo        BOOLEAN       NOT NULL DEFAULT TRUE,
  CONSTRAINT pk_empleado PRIMARY KEY (id_empleado),
  CONSTRAINT uq_empleado_email UNIQUE (email)
);

-- ============================================================

CREATE TABLE transformador (
  id_transformador    INT            NOT NULL AUTO_INCREMENT,
  referencia          VARCHAR(80)    NOT NULL,
  tipo                ENUM('monofasico', 'trifasico', 'autotransformador') NOT NULL,
  potencia_kva        DECIMAL(10,2)  NOT NULL,
  tension_primaria    DECIMAL(10,2)  NOT NULL,
  tension_secundaria  DECIMAL(10,2)  NOT NULL,
  material_bobinado   ENUM('cobre', 'aluminio') NOT NULL,
  estado              ENUM('disponible', 'alquilado', 'mantenimiento', 'vendido') NOT NULL DEFAULT 'disponible',
  stock_disponible    INT            NOT NULL DEFAULT 0,
  precio_venta        DECIMAL(14,2)  NOT NULL,
  precio_alquiler_dia DECIMAL(14,2)  NOT NULL,
  CONSTRAINT pk_transformador PRIMARY KEY (id_transformador),
  CONSTRAINT uq_transformador_ref UNIQUE (referencia),
  CONSTRAINT ck_transformador_stock CHECK (stock_disponible >= 0),
  CONSTRAINT ck_transformador_precio_venta CHECK (precio_venta > 0),
  CONSTRAINT ck_transformador_precio_alquiler CHECK (precio_alquiler_dia > 0)
);

-- ============================================================
-- MÓDULO 2 - CONTACTO Y TRANSACCIONES
-- Ahora PEDIDO es la tabla CENTRAL que unifica agendamiento + pedido
-- ============================================================

CREATE TABLE pedido (
  id_pedido               INT           NOT NULL AUTO_INCREMENT,
  id_cliente              INT           NOT NULL,
  id_empleado             INT           NOT NULL,
  id_transformador        INT           NOT NULL,
  
  -- Tipo y estado del pedido
  tipo_pedido             ENUM('compra', 'alquiler', 'mantenimiento', 'reparacion') NOT NULL,
  estado                  ENUM('en_proceso', 'completado', 'cancelado') NOT NULL DEFAULT 'en_proceso',
  estado_pago             ENUM('no_pagado', 'seña_pagada', 'pagado') NOT NULL DEFAULT 'no_pagado',
  
  -- Información de cita/visita (antes en agendamiento)
  fecha_hora_visita       DATETIME      NULL,
  observaciones           TEXT          NULL,
  
  -- Información de entrega
  monto_total             DECIMAL(14,2) NOT NULL,
  fecha_pedido            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_entrega_estimada  DATETIME      NULL,
  fecha_entrega_real      DATETIME      NULL,
  
  -- Control de auditoría
  updated_at              TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  CONSTRAINT pk_pedido PRIMARY KEY (id_pedido),
  CONSTRAINT fk_pedido_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES cliente (id_cliente)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pedido_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES empleado (id_empleado)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_pedido_transformador
    FOREIGN KEY (id_transformador)
    REFERENCES transformador (id_transformador)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_pedido_monto CHECK (monto_total > 0),
  
  -- Índices para búsquedas frecuentes
  INDEX idx_pedido_cliente (id_cliente),
  INDEX idx_pedido_estado_pago (estado_pago),
  INDEX idx_pedido_fecha (fecha_pedido)
);

-- ============================================================

CREATE TABLE interaccion_chatbot (
  id_interaccion    INT          NOT NULL AUTO_INCREMENT,
  id_pedido         INT          NOT NULL,
  id_cliente        INT          NOT NULL,
  canal             ENUM('whatsapp', 'web', 'email') NOT NULL,
  mensaje_usuario   TEXT         NOT NULL,
  respuesta_bot     TEXT         NOT NULL,
  fecha_interaccion TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_interaccion_chatbot PRIMARY KEY (id_interaccion),
  CONSTRAINT fk_interaccion_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_interaccion_cliente
    FOREIGN KEY (id_cliente)
    REFERENCES cliente (id_cliente)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  INDEX idx_interaccion_pedido (id_pedido),
  INDEX idx_interaccion_cliente (id_cliente)
);

-- ============================================================
-- MÓDULO 3 - DOCUMENTOS DE RETAIL
-- ============================================================

CREATE TABLE cotizacion (
  id_cotizacion      INT           NOT NULL AUTO_INCREMENT,
  id_pedido          INT           NOT NULL,
  id_empleado        INT           NOT NULL,
  numero_cotizacion  VARCHAR(40)   NOT NULL,
  subtotal           DECIMAL(14,2) NOT NULL,
  iva                DECIMAL(14,2) NOT NULL DEFAULT 0,
  total              DECIMAL(14,2) NOT NULL,
  estado             ENUM('borrador', 'enviada', 'aceptada', 'rechazada', 'vencida') NOT NULL DEFAULT 'borrador',
  fecha_emision      TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  fecha_vencimiento  DATETIME      NOT NULL,
  CONSTRAINT pk_cotizacion PRIMARY KEY (id_cotizacion),
  CONSTRAINT uq_cotizacion_pedido UNIQUE (id_pedido),
  CONSTRAINT uq_cotizacion_numero UNIQUE (numero_cotizacion),
  CONSTRAINT fk_cotizacion_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_cotizacion_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES empleado (id_empleado)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_cotizacion_subtotal CHECK (subtotal > 0),
  CONSTRAINT ck_cotizacion_total CHECK (total > 0)
);

-- ============================================================

CREATE TABLE ficha_tecnica (
  id_ficha                INT          NOT NULL AUTO_INCREMENT,
  id_pedido               INT          NOT NULL,
  id_transformador        INT          NOT NULL,
  especificaciones        TEXT         NOT NULL,
  normas_aplicables       VARCHAR(255) NOT NULL,
  condiciones_instalacion TEXT         NULL,
  fecha_generacion        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_ficha_tecnica PRIMARY KEY (id_ficha),
  CONSTRAINT fk_ficha_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_ficha_transformador
    FOREIGN KEY (id_transformador)
    REFERENCES transformador (id_transformador)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

-- ============================================================

CREATE TABLE orden_pedido (
  id_orden              INT           NOT NULL AUTO_INCREMENT,
  id_pedido             INT           NOT NULL,
  id_cotizacion         INT           NOT NULL,
  numero_orden          VARCHAR(40)   NOT NULL,
  metodo_pago           ENUM('transferencia', 'efectivo', 'cheque', 'credito') NOT NULL,
  id_transferencia      VARCHAR(120)  NULL,
  monto_pagado          DECIMAL(14,2) NOT NULL,
  estado                ENUM('pendiente', 'confirmado', 'anulado') NOT NULL DEFAULT 'pendiente',
  fecha_confirmacion    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at            TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  
  CONSTRAINT pk_orden_pedido PRIMARY KEY (id_orden),
  CONSTRAINT uq_orden_pedido UNIQUE (id_pedido),
  CONSTRAINT uq_orden_cotizacion UNIQUE (id_cotizacion),
  CONSTRAINT uq_orden_numero UNIQUE (numero_orden),
  CONSTRAINT fk_orden_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_orden_cotizacion
    FOREIGN KEY (id_cotizacion)
    REFERENCES cotizacion (id_cotizacion)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_orden_monto CHECK (monto_pagado > 0)
);

-- ============================================================
-- MÓDULO 4 - INVENTARIO Y FINANZAS
-- ============================================================

CREATE TABLE movimiento_inventario (
  id_movimiento     INT          NOT NULL AUTO_INCREMENT,
  id_transformador  INT          NOT NULL,
  id_pedido         INT          NULL,
  id_empleado       INT          NOT NULL,
  tipo_movimiento   ENUM('entrada', 'salida_venta', 'salida_alquiler', 'devolucion_alquiler', 'ajuste_inventario') NOT NULL,
  cantidad          INT          NOT NULL,
  fecha_movimiento  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  observaciones     TEXT         NULL,
  CONSTRAINT pk_movimiento_inventario PRIMARY KEY (id_movimiento),
  CONSTRAINT fk_movimiento_transformador
    FOREIGN KEY (id_transformador)
    REFERENCES transformador (id_transformador)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_movimiento_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_movimiento_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES empleado (id_empleado)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_movimiento_cantidad CHECK (cantidad > 0),
  INDEX idx_movimiento_transformador (id_transformador),
  INDEX idx_movimiento_pedido (id_pedido)
);

-- ============================================================

CREATE TABLE registro_financiero (
  id_registro       INT           NOT NULL AUTO_INCREMENT,
  id_pedido         INT           NOT NULL,
  id_empleado       INT           NOT NULL,
  monto             DECIMAL(14,2) NOT NULL,
  tipo_transaccion  ENUM('ingreso_venta', 'ingreso_alquiler', 'ingreso_mantenimiento', 'egreso_proveedor', 'egreso_devolucion') NOT NULL,
  metodo_pago       ENUM('transferencia', 'efectivo', 'cheque', 'credito') NOT NULL,
  estado_pago       ENUM('pendiente', 'completado', 'fallido', 'reembolsado') NOT NULL DEFAULT 'pendiente',
  fecha_transaccion TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comprobante       VARCHAR(180)  NULL,
  CONSTRAINT pk_registro_financiero PRIMARY KEY (id_registro),
  CONSTRAINT fk_registro_pedido
    FOREIGN KEY (id_pedido)
    REFERENCES pedido (id_pedido)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_registro_empleado
    FOREIGN KEY (id_empleado)
    REFERENCES empleado (id_empleado)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT ck_registro_monto CHECK (monto > 0),
  INDEX idx_registro_pedido (id_pedido),
  INDEX idx_registro_estado (estado_pago)
);

-- ============================================================
-- TABLA DE AUDITORÍA (LOGS)
-- ============================================================

CREATE TABLE auditoria_log (
    id_log        INT NOT NULL AUTO_INCREMENT,
    id_empleado   INT NULL, -- Puede ser NULL si es un sistema automático
    accion        ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    tabla_nombre  VARCHAR(50) NOT NULL,
    registro_id   INT NOT NULL,
    detalle       TEXT NULL, -- Aquí guardaremos los cambios
    fecha         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT pk_auditoria PRIMARY KEY (id_log),
    CONSTRAINT fk_auditoria_empleado FOREIGN KEY (id_empleado) REFERENCES empleado (id_empleado)
);

-- ============================================================
-- TRIGGERS AUTOMÁTICOS
-- ============================================================

DELIMITER $$

-- ============================================================
-- TRIGGER 1: Actualizar stock automáticamente después de movimiento_inventario
-- Propósito: Mantener stock_disponible sincronizado automáticamente
-- ============================================================
CREATE TRIGGER trg_actualizar_stock_despues_movimiento
AFTER INSERT ON movimiento_inventario
FOR EACH ROW
BEGIN
  DECLARE nuevo_stock INT;
  DECLARE stock_actual INT;
  
  -- Obtener stock actual
  SELECT stock_disponible INTO stock_actual
  FROM transformador
  WHERE id_transformador = NEW.id_transformador;
  
  -- Calcular nuevo stock según tipo de movimiento
  IF NEW.tipo_movimiento = 'entrada' THEN
    SET nuevo_stock = stock_actual + NEW.cantidad;
  ELSEIF NEW.tipo_movimiento IN ('salida_venta', 'salida_alquiler') THEN
    SET nuevo_stock = stock_actual - NEW.cantidad;
  ELSEIF NEW.tipo_movimiento = 'devolucion_alquiler' THEN
    SET nuevo_stock = stock_actual + NEW.cantidad;
  ELSEIF NEW.tipo_movimiento = 'ajuste_inventario' THEN
    SET nuevo_stock = stock_actual + NEW.cantidad;
  ELSE
    SET nuevo_stock = stock_actual;
  END IF;
  
  -- Validar que no sea negativo
  IF nuevo_stock < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Stock no puede ser negativo después del movimiento';
  END IF;
  
  -- Actualizar stock
  UPDATE transformador
  SET stock_disponible = nuevo_stock
  WHERE id_transformador = NEW.id_transformador;
END$$

-- ============================================================
-- TRIGGER 2: Validar stock disponible ANTES de completar pedido
-- Propósito: Evitar que se completen pedidos sin stock disponible
-- ============================================================
CREATE TRIGGER trg_validar_stock_antes_completar_pedido
BEFORE UPDATE ON pedido
FOR EACH ROW
BEGIN
  DECLARE stock_disponible_actual INT;
  
  -- Solo validar si el estado cambia a "completado"
  IF NEW.estado = 'completado' AND OLD.estado != 'completado' THEN
    
    -- Obtener stock disponible
    SELECT stock_disponible INTO stock_disponible_actual
    FROM transformador
    WHERE id_transformador = NEW.id_transformador;
    
    -- Validar según tipo de pedido
    IF NEW.tipo_pedido = 'compra' AND stock_disponible_actual <= 0 THEN
      SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'Stock insuficiente para completar venta. No hay transformadores disponibles.';
    END IF;
  END IF;
END$$

-- ============================================================
-- TRIGGER 3: Crear movimiento_inventario automático cuando pedido se completa
-- Propósito: Registrar automáticamente la salida de inventario
-- ============================================================
CREATE TRIGGER trg_crear_movimiento_pedido_completado
AFTER UPDATE ON pedido
FOR EACH ROW
BEGIN
  DECLARE tipo_mov VARCHAR(50);
  
  -- Solo procesar cuando el pedido pasa a "completado"
  IF NEW.estado = 'completado' AND OLD.estado != 'completado' THEN
    
    -- Determinar tipo de movimiento según tipo de pedido
    IF NEW.tipo_pedido = 'compra' THEN
      SET tipo_mov = 'salida_venta';
    ELSEIF NEW.tipo_pedido = 'alquiler' THEN
      SET tipo_mov = 'salida_alquiler';
    ELSE
      SET tipo_mov = 'ajuste_inventario';
    END IF;
    
    -- Crear registro de movimiento automático
    INSERT INTO movimiento_inventario (
      id_transformador,
      id_pedido,
      id_empleado,
      tipo_movimiento,
      cantidad,
      fecha_movimiento,
      observaciones
    ) VALUES (
      NEW.id_transformador,
      NEW.id_pedido,
      NEW.id_empleado,
      tipo_mov,
      1,
      NOW(),
      CONCAT('Movimiento automático por completación de pedido #', NEW.id_pedido)
    );
  END IF;
END$$

-- ============================================================
-- TRIGGER 4: Crear cotización automática cuando pedido se crea
-- Propósito: Generar documento comercial automáticamente
-- ============================================================
CREATE TRIGGER trg_crear_cotizacion_pedido_nuevo
AFTER INSERT ON pedido
FOR EACH ROW
BEGIN
  DECLARE precio_unitario DECIMAL(14,2);
  DECLARE subtotal DECIMAL(14,2);
  DECLARE iva_monto DECIMAL(14,2);
  DECLARE total DECIMAL(14,2);
  DECLARE num_cot VARCHAR(40);
  
  -- Obtener precio según tipo de pedido
  IF NEW.tipo_pedido = 'alquiler' THEN
    SELECT precio_alquiler_dia INTO precio_unitario
    FROM transformador
    WHERE id_transformador = NEW.id_transformador;
    SET subtotal = precio_unitario;
  ELSE
    SELECT precio_venta INTO precio_unitario
    FROM transformador
    WHERE id_transformador = NEW.id_transformador;
    SET subtotal = precio_unitario;
  END IF;
  
  -- Calcular IVA y total
  SET iva_monto = subtotal * 0.19;
  SET total = subtotal + iva_monto;
  SET num_cot = CONCAT('COT-', NEW.id_pedido, '-', DATE_FORMAT(NOW(), '%Y%m%d'));
  
  -- Insertar cotización automáticamente
  INSERT INTO cotizacion (
    id_pedido,
    id_empleado,
    numero_cotizacion,
    subtotal,
    iva,
    total,
    estado,
    fecha_vencimiento
  ) VALUES (
    NEW.id_pedido,
    NEW.id_empleado,
    num_cot,
    subtotal,
    iva_monto,
    total,
    'borrador',
    DATE_ADD(NOW(), INTERVAL 30 DAY)
  );
END$$

-- ============================================================
-- TRIGGER 5: Crear ficha técnica automática cuando pedido se crea
-- Propósito: Generar especificaciones técnicas automáticamente
-- ============================================================
CREATE TRIGGER trg_crear_ficha_tecnica_pedido_nuevo
AFTER INSERT ON pedido
FOR EACH ROW
BEGIN
  DECLARE especificaciones TEXT;
  
  -- Construir especificaciones técnicas
  SELECT CONCAT(
    'Tipo: ', tipo, ' | ',
    'Potencia: ', potencia_kva, ' kVA | ',
    'Tensión Primaria: ', tension_primaria, 'V | ',
    'Tensión Secundaria: ', tension_secundaria, 'V | ',
    'Material de bobinado: ', material_bobinado
  ) INTO especificaciones
  FROM transformador
  WHERE id_transformador = NEW.id_transformador;
  
  -- Insertar ficha técnica
  INSERT INTO ficha_tecnica (
    id_pedido,
    id_transformador,
    especificaciones,
    normas_aplicables,
    condiciones_instalacion
  ) VALUES (
    NEW.id_pedido,
    NEW.id_transformador,
    especificaciones,
    'IEC 60076-1, NTC 1393, Resolución 180541 de 2015 (RETIE)',
    'Instalación por personal certificado. Temperatura de operación: -25°C a +55°C. Altitud máxima: 2000m snm. Ambiente ventilado. Protección contra humedad y corrosión.'
  );
END$$

-- ============================================================
-- TRIGGER 6: Actualizar estado_pago cuando orden_pedido se confirma
-- Propósito: Sincronizar estado de pago entre tablas
-- ============================================================
CREATE TRIGGER trg_actualizar_pago_orden_confirmada
AFTER UPDATE ON orden_pedido
FOR EACH ROW
BEGIN
  -- Cuando la orden se confirma, marcar el pedido como pagado
  IF NEW.estado = 'confirmado' AND OLD.estado != 'confirmado' THEN
    UPDATE pedido
    SET estado_pago = 'pagado'
    WHERE id_pedido = NEW.id_pedido;
  END IF;
  
  -- Cuando la orden se anula, revertir a no pagado
  IF NEW.estado = 'anulado' AND OLD.estado != 'anulado' THEN
    UPDATE pedido
    SET estado_pago = 'no_pagado'
    WHERE id_pedido = NEW.id_pedido;
  END IF;
END$$

-- ============================================================
-- TRIGGER 7: Crear registro_financiero automático cuando orden se confirma
-- Propósito: Registrar automáticamente la transacción de pago
-- ============================================================
CREATE TRIGGER trg_crear_registro_financiero_orden_confirmada
AFTER UPDATE ON orden_pedido
FOR EACH ROW
BEGIN
  DECLARE tipo_trans VARCHAR(50);
  DECLARE id_emp INT;
  DECLARE tipo_ped VARCHAR(50);
  
  -- Solo procesar cuando la orden se confirma
  IF NEW.estado = 'confirmado' AND OLD.estado != 'confirmado' THEN
    
    -- Obtener datos del pedido
    SELECT id_empleado, tipo_pedido
    INTO id_emp, tipo_ped
    FROM pedido
    WHERE id_pedido = NEW.id_pedido;
    
    -- Determinar tipo de transacción según tipo de pedido
    IF tipo_ped = 'compra' THEN
      SET tipo_trans = 'ingreso_venta';
    ELSEIF tipo_ped = 'alquiler' THEN
      SET tipo_trans = 'ingreso_alquiler';
    ELSEIF tipo_ped = 'mantenimiento' THEN
      SET tipo_trans = 'ingreso_mantenimiento';
    ELSE
      SET tipo_trans = 'ingreso_venta';
    END IF;
    
    -- Crear registro financiero automático
    INSERT INTO registro_financiero (
      id_pedido,
      id_empleado,
      monto,
      tipo_transaccion,
      metodo_pago,
      estado_pago,
      comprobante
    ) VALUES (
      NEW.id_pedido,
      id_emp,
      NEW.monto_pagado,
      tipo_trans,
      NEW.metodo_pago,
      'completado',
      NEW.numero_orden
    );
  END IF;
END$$

-- ============================================================
-- TRIGGER 8: Validar que cotización esté aceptada antes de crear orden
-- Propósito: Evitar crear orden sin cotización aceptada
-- ============================================================
CREATE TRIGGER trg_validar_cotizacion_antes_orden
BEFORE INSERT ON orden_pedido
FOR EACH ROW
BEGIN
  DECLARE estado_cot VARCHAR(50);
  
  -- Obtener estado de cotización
  SELECT estado INTO estado_cot
  FROM cotizacion
  WHERE id_cotizacion = NEW.id_cotizacion;
  
  -- Validar que esté aceptada
  IF estado_cot NOT IN ('aceptada', 'enviada') THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'No se puede crear orden de pedido. La cotización debe estar aceptada.';
  END IF;
END$$

-- ============================================================
-- TRIGGER 9: Actualizar estado de cotización cuando orden se confirma
-- Propósito: Marcar cotización como aceptada cuando hay pago
-- ============================================================
CREATE TRIGGER trg_actualizar_cotizacion_orden_confirmada
AFTER UPDATE ON orden_pedido
FOR EACH ROW
BEGIN
  IF NEW.estado = 'confirmado' AND OLD.estado != 'confirmado' THEN
    UPDATE cotizacion
    SET estado = 'aceptada'
    WHERE id_cotizacion = NEW.id_cotizacion;
  END IF;
END$$


-- ============================================================
-- TRIGGER 10: Log de cambios en clientes
-- Propósito: Registrar auditoría de todas las operaciones en la tabla cliente
-- ============================================================
CREATE TRIGGER trg_log_cliente_insert
AFTER INSERT ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_log (id_empleado, accion, tabla_nombre, registro_id, detalle)
    VALUES (@usuario_id, 'INSERT', 'cliente', NEW.id_cliente, 
            CONCAT('Nuevo cliente creado: ', NEW.nombre));
END$$

-- Log para CAMBIOS en clientes
CREATE TRIGGER trg_log_cliente_update
AFTER UPDATE ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_log (id_empleado, accion, tabla_nombre, registro_id, detalle)
    VALUES (@usuario_id, 'UPDATE', 'cliente', NEW.id_cliente, 
            CONCAT('Cambio en ', OLD.nombre, '. Email anterior: ', OLD.email, ' -> Nuevo: ', NEW.email));
END$$

-- Log para ELIMINACIÓN de clientes
CREATE TRIGGER trg_log_cliente_delete
AFTER DELETE ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria_log (id_empleado, accion, tabla_nombre, registro_id, detalle)
    VALUES (@usuario_id, 'DELETE', 'cliente', OLD.id_cliente, 
            CONCAT('Cliente eliminado: ', OLD.nombre));
END$$

DELIMITER ;

-- ============================================================
-- ÍNDICES ADICIONALES PARA PERFORMANCE
-- ============================================================

CREATE INDEX idx_orden_pedido_estado ON orden_pedido(estado);
CREATE INDEX idx_cotizacion_estado ON cotizacion(estado);
CREATE INDEX idx_interaccion_fecha ON interaccion_chatbot(fecha_interaccion);

-- ============================================================
-- ============================================================
-- DATOS DE PRUEBA - COHERENTES Y COMPLETOS
-- Para probar TODOS los triggers automáticos
-- ============================================================
-- ============================================================

-- ============================================================
-- PASO 1: Insertar CLIENTES
-- ============================================================
INSERT INTO cliente (nombre, empresa, email, telefono, tipo_cliente) VALUES
('Carlos González Pérez', 'Empresa Constructora ABC', 'carlos.gonzalez@constructora.com', '+573015555001', 'corporativo'),
('María Rodriguez López', 'Industrias Mecánicas XYZ', 'maria.rodriguez@mecanica.com', '+573105555002', 'corporativo'),
('Juan Felipe Martínez', 'Comercio Individual', 'juan.martinez@email.com', '+573215555003', 'individual'),
('Laura Sánchez Torres', 'Gobierno - Alcaldía Bogotá', 'laura.sanchez@alcaldia.gov.co', '+573315555004', 'gobierno'),
('Roberto Díaz Castro', 'Distribuidora Eléctrica Sur', 'roberto.diaz@distribuidora.com', '+573415555005', 'corporativo'),
('Paola Cortés Gómez', 'PYME Eléctrica Colombia', 'paola.cortes@pymelectrica.com', '+573515555006', 'individual');

-- ============================================================
-- PASO 2: Insertar EMPLEADOS
-- ============================================================
INSERT INTO empleado (nombre, email, rol, area, activo) VALUES
('Andrés Felipe Lázaro', 'andres.lazaro@induelectro.com', 'gerente', 'gerencia', TRUE),
('Jhon Alexander Hernández', 'jhon.hernandez@induelectro.com', 'administrativo', 'atencion_cliente', TRUE),
('Yeferson Alejandro Acosta', 'yeferson.acosta@induelectro.com', 'tecnico', 'tecnica', TRUE),
('María Gómez Rodríguez', 'maria.gomez@induelectro.com', 'chatbot', 'atencion_cliente', TRUE),
('Carlos Ruiz Técnico', 'carlos.ruiz@induelectro.com', 'tecnico', 'tecnica', TRUE),
('Sandra López Admin', 'sandra.lopez@induelectro.com', 'administrativo', 'administrativa', TRUE);

-- ============================================================
-- PASO 3: Insertar TRANSFORMADORES (diversos tipos y potencias)
-- ============================================================
INSERT INTO transformador (referencia, tipo, potencia_kva, tension_primaria, tension_secundaria, material_bobinado, estado, stock_disponible, precio_venta, precio_alquiler_dia) VALUES
('TRAF-50-MONO-CU-001', 'monofasico', 50.00, 220.00, 110.00, 'cobre', 'disponible', 5, 1500000.00, 50000.00),
('TRAF-100-TRIFASICO-CU-002', 'trifasico', 100.00, 440.00, 220.00, 'cobre', 'disponible', 3, 3000000.00, 100000.00),
('TRAF-25-MONO-AL-003', 'monofasico', 25.00, 220.00, 110.00, 'aluminio', 'disponible', 8, 800000.00, 30000.00),
('TRAF-75-TRIFASICO-CU-004', 'trifasico', 75.00, 440.00, 220.00, 'cobre', 'disponible', 2, 2200000.00, 80000.00),
('TRAF-150-TRIFASICO-CU-005', 'trifasico', 150.00, 440.00, 220.00, 'cobre', 'disponible', 1, 4500000.00, 150000.00),
('TRAF-200-AUTO-CU-006', 'autotransformador', 200.00, 440.00, 220.00, 'cobre', 'disponible', 0, 6000000.00, 200000.00);

-- ============================================================
-- PASO 4: Insertar PEDIDOS (diferentes escenarios)
-- TRIGGER 4 y 5 crearán COTIZACIÓN y FICHA_TÉCNICA automáticamente
-- ============================================================

-- PEDIDO 1: COMPRA - sin pagar (estado_pago: no_pagado)
INSERT INTO pedido (id_cliente, id_empleado, id_transformador, tipo_pedido, estado, estado_pago, fecha_hora_visita, observaciones, monto_total) 
VALUES (1, 2, 1, 'compra', 'en_proceso', 'no_pagado', '2026-05-05 14:00:00', 'Cliente interesado en transformador de 50 kVA monofásico cobre', 1500000.00);

-- PEDIDO 2: ALQUILER - sin pagar
INSERT INTO pedido (id_cliente, id_empleado, id_transformador, tipo_pedido, estado, estado_pago, fecha_hora_visita, observaciones, monto_total) 
VALUES (2, 2, 2, 'alquiler', 'en_proceso', 'no_pagado', '2026-05-06 10:00:00', 'Alquiler por 30 días para proyecto temporal de industria', 3000000.00);

-- PEDIDO 3: COMPRA - con seña pagada
INSERT INTO pedido (id_cliente, id_empleado, id_transformador, tipo_pedido, estado, estado_pago, fecha_hora_visita, observaciones, monto_total) 
VALUES (3, 2, 3, 'compra', 'en_proceso', 'seña_pagada', '2026-05-07 09:00:00', 'Cliente ha depositado seña de 300000 COP el 30 de abril', 800000.00);

-- PEDIDO 4: COMPRA - COMPLETAMENTE PAGADO (100%)
INSERT INTO pedido (id_cliente, id_empleado, id_transformador, tipo_pedido, estado, estado_pago, fecha_hora_visita, observaciones, monto_total) 
VALUES (4, 3, 4, 'compra', 'en_proceso', 'pagado', '2026-05-08 11:00:00', 'Cliente municipal pagó el 100% el 28 de abril. Listo para orden', 2200000.00);

-- PEDIDO 5: MANTENIMIENTO - sin pagar
INSERT INTO pedido (id_cliente, id_empleado, id_transformador, tipo_pedido, estado, estado_pago, fecha_hora_visita, observaciones, monto_total) 
VALUES (5, 3, 5, 'mantenimiento', 'en_proceso', 'no_pagado', '2026-05-10 15:00:00', 'Servicio de mantenimiento preventivo y revisión técnica completa', 500000.00);

-- PEDIDO 6: COMPRA - COMPLETADO Y PAGADO (flujo completo)
INSERT INTO pedido (id_cliente, id_empleado, id_transformador, tipo_pedido, estado, estado_pago, fecha_hora_visita, observaciones, monto_total, fecha_entrega_real) 
VALUES (6, 4, 1, 'compra', 'completado', 'pagado', '2026-04-20 13:00:00', 'Entregado exitosamente el 25 de abril. Cliente totalmente satisfecho.', 1500000.00, '2026-04-25 16:30:00');

-- ============================================================
-- PASO 5: Insertar INTERACCIONES CHATBOT
-- ============================================================

-- Interacciones del Pedido 1
INSERT INTO interaccion_chatbot (id_pedido, id_cliente, canal, mensaje_usuario, respuesta_bot) VALUES
(1, 1, 'whatsapp', '¿Tienen transformadores de 50 kVA monofásico?', 'Sí, contamos con transformadores monofásicos de 50 kVA en cobre y aluminio. Precio: $1.500.000 COP. ¿De qué tipo?'),
(1, 1, 'whatsapp', 'Necesito monofásico de cobre de buena calidad', 'Perfecto. Tenemos TRAF-50-MONO-CU-001. Precio: $1.500.000 COP + IVA ($285.000) = $1.785.000 total. ¿Desea cotización?'),
(1, 1, 'whatsapp', 'Sí, envíeme la cotización por favor', 'Cotización generada automáticamente: COT-1-20260430. Vencimiento: 30 días. Se envía a su email registrado.');

-- Interacciones del Pedido 2
INSERT INTO interaccion_chatbot (id_pedido, id_cliente, canal, mensaje_usuario, respuesta_bot) VALUES
(2, 2, 'web', '¿Pueden rentar un transformador trifásico de 100 kVA?', 'Sí, disponemos de TRAF-100-TRIFASICO-CU-002. Costo de alquiler: $100.000 COP/día. ¿Por cuántos días lo necesita?'),
(2, 2, 'web', 'Necesito por aproximadamente 30 días para un proyecto', 'Costo total estimado: $3.000.000 COP (30 días × $100.000/día). ¿Confirma el alquiler?'),
(2, 2, 'web', 'Sí, adelante con la cotización', 'Cotización de alquiler generada: COT-2-20260430. Plazo de vigencia: 30 días.');

-- Interacciones del Pedido 3
INSERT INTO interaccion_chatbot (id_pedido, id_cliente, canal, mensaje_usuario, respuesta_bot) VALUES
(3, 3, 'email', 'Me interesa un transformador de 25 kVA aluminio para mi negocio', 'Disponible TRAF-25-MONO-AL-003. Precio: $800.000 COP + IVA = $952.000 total. Excelente relación precio-potencia. ¿Desea cotización?'),
(3, 3, 'email', 'Sí, genere la cotización', 'Cotización COT-3-20260430 enviada a su email. Requiere depósito inicial del 30-40% para reservar el equipo.');

-- Interacciones del Pedido 4
INSERT INTO interaccion_chatbot (id_pedido, id_cliente, canal, mensaje_usuario, respuesta_bot) VALUES
(4, 4, 'whatsapp', 'Necesitamos transformador para proyecto municipal de electrificación', 'Contamos con TRAF-75-TRIFASICO-CU-004 (75 kVA). Precio: $2.200.000 COP + IVA = $2.618.000. ¿Le interesa?'),
(4, 4, 'whatsapp', 'Sí, enviamos cotización a nuestra oficina de compras', 'Cotización COT-4-20260430 enviada. El pago se confirmó el 28 de abril mediante transferencia. Procederemos con orden de pedido.'),
(4, 4, 'whatsapp', 'Perfecto, adelante con el proceso completo', 'Excelente. Orden de pedido ORD-4-20260430 ha sido generada. Procederemos con la preparación y entrega.');

-- Interacciones del Pedido 5
INSERT INTO interaccion_chatbot (id_pedido, id_cliente, canal, mensaje_usuario, respuesta_bot) VALUES
(5, 5, 'web', '¿Hacen servicio de mantenimiento de transformadores?', 'Sí, ofrecemos mantenimiento preventivo, correctivo y revisiones técnicas. Costo: desde $500.000 COP según tipo de servicio.'),
(5, 5, 'web', 'Necesito revisión técnica completa de mis transformadores de 150 kVA', 'Para TRAF-150-TRIFASICO-CU-005, la revisión completa (inspección visual, pruebas eléctricas, limpieza) cuesta $500.000 COP. ¿Confirma?'),
(5, 5, 'web', 'Sí, genere la cotización por favor', 'Cotización de mantenimiento COT-5-20260430 generada. Nuestro técnico se contactará para agendar la visita.');

-- Interacciones del Pedido 6
INSERT INTO interaccion_chatbot (id_pedido, id_cliente, canal, mensaje_usuario, respuesta_bot) VALUES
(6, 6, 'email', 'Necesito transformador de 50 kVA para ampliar mi instalación eléctrica', 'TRAF-50-MONO-CU-001 disponible. Precio: $1.500.000 + IVA = $1.785.000. ¿Procede?'),
(6, 6, 'email', 'Sí, adelante con todo el proceso', 'Cotización COT-6-20260425 generada. El cliente pagó el 24 de abril. Orden de pedido ORD-6-20260425 emitida.');

-- ============================================================
-- PASO 6: Actualizar COTIZACIONES a 'aceptada' para permitir crear ORDEN
-- (Necesario porque TRIGGER 8 valida que esté aceptada)
-- ============================================================
UPDATE cotizacion SET estado = 'aceptada' WHERE id_pedido = 4;
UPDATE cotizacion SET estado = 'aceptada' WHERE id_pedido = 6;

-- ============================================================
-- PASO 7: Crear ORDEN_PEDIDO (dispara TRIGGER 6, 7, 9)
-- ============================================================

-- Orden para Pedido 4 (PAGADO + COTIZACIÓN ACEPTADA)
INSERT INTO orden_pedido (id_pedido, id_cotizacion, numero_orden, metodo_pago, monto_pagado, estado) 
VALUES (4, 4, 'ORD-4-20260430', 'transferencia', 2200000.00, 'confirmado');

-- Orden para Pedido 6
INSERT INTO orden_pedido (id_pedido, id_cotizacion, numero_orden, metodo_pago, monto_pagado, estado) 
VALUES (6, 6, 'ORD-6-20260425', 'efectivo', 1500000.00, 'confirmado');

-- ============================================================
-- PASO 8: Completar Pedido 6 (dispara TRIGGER 2, 3, 1)
-- ============================================================
UPDATE pedido SET estado = 'completado' WHERE id_pedido = 6;

-- ============================================================
-- FIN DEL SCRIPT - BD LISTA PARA PRUEBAS
-- ============================================================