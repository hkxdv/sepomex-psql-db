-- Tablas con codificación y validaciones correctas
-- Tabla de estados
CREATE TABLE estados (
    codigo_estado CHAR(2) PRIMARY KEY,
    nombre_estado VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_codigo_estado CHECK (codigo_estado ~ '^[0-9]{2}$')
) WITH (FILLFACTOR = 90);

-- Tabla de municipios
CREATE TABLE municipios (
    codigo_municipio CHAR(3),
    codigo_estado CHAR(2),
    nombre_municipio VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (codigo_municipio, codigo_estado),
    FOREIGN KEY (codigo_estado) REFERENCES estados(codigo_estado),
    CONSTRAINT chk_codigo_municipio CHECK (codigo_municipio ~ '^[0-9]{3}$')
) WITH (FILLFACTOR = 90);

-- Tabla de ciudades
CREATE TABLE ciudades (
    codigo_ciudad CHAR(2),
    codigo_estado CHAR(2),
    nombre_ciudad VARCHAR(100) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (codigo_ciudad, codigo_estado),
    FOREIGN KEY (codigo_estado) REFERENCES estados(codigo_estado),
    CONSTRAINT chk_codigo_ciudad CHECK (codigo_ciudad ~ '^[0-9]{2}$')
) WITH (FILLFACTOR = 90);

-- Tabla de tipos de asentamiento
CREATE TABLE tipos_asentamiento (
    codigo_tipo_asentamiento CHAR(2) PRIMARY KEY,
    nombre_tipo_asentamiento VARCHAR(50) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_codigo_tipo_asentamiento CHECK (codigo_tipo_asentamiento ~ '^[0-9]{2}$')
) WITH (FILLFACTOR = 90);

-- Tabla de zonas
CREATE TABLE zonas (
    id_zona SERIAL PRIMARY KEY,
    tipo_zona VARCHAR(20) NOT NULL UNIQUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_tipo_zona CHECK (tipo_zona IN ('Urbano', 'Rural', 'Semiurbano'))
) WITH (FILLFACTOR = 90);

-- Tabla principal de códigos postales
CREATE TABLE codigos_postales (
    id_codigo_postal SERIAL PRIMARY KEY,
    codigo_postal CHAR(5) NOT NULL,
    nombre_asentamiento VARCHAR(100) NOT NULL,
    codigo_estado CHAR(2),
    codigo_municipio CHAR(3),
    codigo_ciudad CHAR(2),
    codigo_tipo_asentamiento CHAR(2),
    id_zona INTEGER,
    codigo_postal_administracion CHAR(5) NOT NULL,
    codigo_oficina_postal CHAR(5),
    id_asentamiento_consecutivo CHAR(4),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (codigo_estado) REFERENCES estados(codigo_estado),
    FOREIGN KEY (codigo_municipio, codigo_estado) REFERENCES municipios(codigo_municipio, codigo_estado),
    FOREIGN KEY (codigo_ciudad, codigo_estado) REFERENCES ciudades(codigo_ciudad, codigo_estado),
    FOREIGN KEY (codigo_tipo_asentamiento) REFERENCES tipos_asentamiento(codigo_tipo_asentamiento),
    FOREIGN KEY (id_zona) REFERENCES zonas(id_zona),
    CONSTRAINT chk_codigo_postal CHECK (codigo_postal ~ '^[0-9]{5}$'),
    CONSTRAINT chk_codigo_postal_admin CHECK (codigo_postal_administracion ~ '^[0-9]{5}$'),
    CONSTRAINT chk_codigo_oficina CHECK (codigo_oficina_postal IS NULL OR codigo_oficina_postal ~ '^[0-9]{5}$'),
    CONSTRAINT chk_id_asentamiento CHECK (id_asentamiento_consecutivo ~ '^[0-9]{4}$')
) WITH (FILLFACTOR = 90);