/**
 * @file functions.sql
 * @description Funciones PL/pgSQL para la base de datos v2 del proyecto SEPOMEX.
 */

/**
 * @function: search_settlements_by_name
 * @description: Busca asentamientos por nombre con paginación, usado en /api/v2/postal/search?query={query}&limit={limit}&offset={offset}.
 * @param p_query: Término de búsqueda (máx. 100 caracteres).
 * @param p_limit: Límite de registros por página (1-100).
 * @param p_offset: Desplazamiento para paginación (>=0).
 * @returns: Tabla con estructura PostalCodeRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION search_settlements_by_name(
    p_query VARCHAR(100),
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    codigo_postal CHAR(5),
    nombre_asentamiento VARCHAR(100),
    tipo_asentamiento VARCHAR(50),
    zona VARCHAR(20),
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50),
    pk_codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    pk_codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50)
) AS $$
BEGIN
    IF p_limit < 1 OR p_limit > 100 THEN
        RAISE EXCEPTION 'El límite debe estar entre 1 y 100';
    END IF;
    IF p_offset < 0 THEN
        RAISE EXCEPTION 'El offset debe ser mayor o igual a 0';
    END IF;

    RETURN QUERY
    SELECT
        vm.codigo_postal,
        vm.nombre_asentamiento,
        vm.nombre_tipo_asentamiento AS tipo_asentamiento,
        vm.nombre_zona AS zona,
        vm.codigo_estado,
        vm.nombre_estado,
        vm.codigo_municipio AS pk_codigo_municipio,
        vm.nombre_municipio,
        vm.codigo_ciudad AS pk_codigo_ciudad,
        vm.nombre_ciudad
    FROM vm_codigos_postales vm
    WHERE vm.nombre_asentamiento ILIKE '%' || p_query || '%'
    ORDER BY vm.nombre_asentamiento
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: search_by_postal_code
 * @description: Busca códigos postales por código exacto, usado en /api/v2/postal/codigo/{code}.
 * @param p_codigo_postal: Código postal (5 dígitos).
 * @returns: Tabla con estructura PostalCodeRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION search_by_postal_code(
    p_codigo_postal VARCHAR(5) -- Acepta VARCHAR para facilitar la validación, pero busca CHAR(5)
)
RETURNS TABLE (
    codigo_postal CHAR(5),
    nombre_asentamiento VARCHAR(100),
    tipo_asentamiento VARCHAR(50),
    zona VARCHAR(20),
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50),
    pk_codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    pk_codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50)
) AS $$
BEGIN
    IF p_codigo_postal !~ '^[0-9]{5}$' THEN
        RAISE EXCEPTION 'El código postal debe ser de 5 dígitos';
    END IF;

    RETURN QUERY
    SELECT
        vm.codigo_postal,
        vm.nombre_asentamiento,
        vm.nombre_tipo_asentamiento AS tipo_asentamiento,
        vm.nombre_zona AS zona,
        vm.codigo_estado,
        vm.nombre_estado,
        vm.codigo_municipio AS pk_codigo_municipio,
        vm.nombre_municipio,
        vm.codigo_ciudad AS pk_codigo_ciudad,
        vm.nombre_ciudad
    FROM vm_codigos_postales vm
    WHERE vm.codigo_postal = p_codigo_postal::CHAR(5) -- Cast a CHAR para coincidir con la tabla/vista
    ORDER BY vm.nombre_asentamiento;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_postal_codes_by_state
 * @description: Lista códigos postales por estado con paginación, usado en /api/v2/postal/estado/{estadoId} y /api/v2/estado/{estadoId}/asentamientos.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @param p_limit: Límite de registros por página (1-100).
 * @param p_offset: Desplazamiento para paginación (>=0).
 * @returns: Tabla con estructura PostalCodeRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_postal_codes_by_state(
    p_codigo_estado VARCHAR(2), -- Acepta VARCHAR para facilitar la validación
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    codigo_postal CHAR(5),
    nombre_asentamiento VARCHAR(100),
    tipo_asentamiento VARCHAR(50),
    zona VARCHAR(20),
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50),
    pk_codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    pk_codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;
    IF p_limit < 1 OR p_limit > 100 THEN
        RAISE EXCEPTION 'El límite debe estar entre 1 y 100';
    END IF;
    IF p_offset < 0 THEN
        RAISE EXCEPTION 'El offset debe ser mayor o igual a 0';
    END IF;

    RETURN QUERY
    SELECT
        vm.codigo_postal,
        vm.nombre_asentamiento,
        vm.nombre_tipo_asentamiento AS tipo_asentamiento,
        vm.nombre_zona AS zona,
        vm.codigo_estado,
        vm.nombre_estado,
        vm.codigo_municipio AS pk_codigo_municipio,
        vm.nombre_municipio,
        vm.codigo_ciudad AS pk_codigo_ciudad,
        vm.nombre_ciudad
    FROM vm_codigos_postales vm
    WHERE vm.codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    ORDER BY vm.codigo_postal, vm.nombre_asentamiento
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_postal_codes_by_municipality
 * @description: Lista códigos postales por municipio con paginación, usado en /api/v2/postal/municipio/{estadoId}/{municipioId}.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @param p_codigo_municipio: Código del municipio (3 dígitos).
 * @param p_limit: Límite de registros por página (1-100).
 * @param p_offset: Desplazamiento para paginación (>=0).
 * @returns: Tabla con estructura PostalCodeRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_postal_codes_by_municipality(
    p_codigo_estado VARCHAR(2), -- Acepta VARCHAR
    p_codigo_municipio VARCHAR(3), -- Acepta VARCHAR
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    codigo_postal CHAR(5),
    nombre_asentamiento VARCHAR(100),
    tipo_asentamiento VARCHAR(50),
    zona VARCHAR(20),
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50),
    pk_codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    pk_codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;
    IF p_codigo_municipio !~ '^[0-9]{3}$' THEN
        RAISE EXCEPTION 'El código de municipio debe ser de 3 dígitos';
    END IF;
    IF p_limit < 1 OR p_limit > 100 THEN
        RAISE EXCEPTION 'El límite debe estar entre 1 y 100';
    END IF;
    IF p_offset < 0 THEN
        RAISE EXCEPTION 'El offset debe ser mayor o igual a 0';
    END IF;

    RETURN QUERY
    SELECT
        vm.codigo_postal,
        vm.nombre_asentamiento,
        vm.nombre_tipo_asentamiento AS tipo_asentamiento,
        vm.nombre_zona AS zona,
        vm.codigo_estado,
        vm.nombre_estado,
        vm.codigo_municipio AS pk_codigo_municipio,
        vm.nombre_municipio,
        vm.codigo_ciudad AS pk_codigo_ciudad,
        vm.nombre_ciudad
    FROM vm_codigos_postales vm
    WHERE vm.codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    AND vm.codigo_municipio = p_codigo_municipio::CHAR(3) -- Cast a CHAR
    ORDER BY vm.codigo_postal, vm.nombre_asentamiento
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_postal_codes_by_city
 * @description: Lista códigos postales por ciudad con paginación, usado en /api/v2/postal/ciudad/{estadoId}/{ciudadId} y /api/v2/ciudad/{estadoId}/{ciudadId}/codigos.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @param p_codigo_ciudad: Código de la ciudad (2 dígitos).
 * @param p_limit: Límite de registros por página (1-100).
 * @param p_offset: Desplazamiento para paginación (>=0).
 * @returns: Tabla con estructura PostalCodeRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_postal_codes_by_city(
    p_codigo_estado VARCHAR(2), -- Acepta VARCHAR
    p_codigo_ciudad VARCHAR(2), -- Acepta VARCHAR
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    codigo_postal CHAR(5),
    nombre_asentamiento VARCHAR(100),
    tipo_asentamiento VARCHAR(50),
    zona VARCHAR(20),
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50),
    pk_codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    pk_codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;
    IF p_codigo_ciudad !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de ciudad debe ser de 2 dígitos';
    END IF;
    IF p_limit < 1 OR p_limit > 100 THEN
        RAISE EXCEPTION 'El límite debe estar entre 1 y 100';
    END IF;
    IF p_offset < 0 THEN
        RAISE EXCEPTION 'El offset debe ser mayor o igual a 0';
    END IF;

    RETURN QUERY
    SELECT
        vm.codigo_postal,
        vm.nombre_asentamiento,
        vm.nombre_tipo_asentamiento AS tipo_asentamiento,
        vm.nombre_zona AS zona,
        vm.codigo_estado,
        vm.nombre_estado,
        vm.codigo_municipio AS pk_codigo_municipio,
        vm.nombre_municipio,
        vm.codigo_ciudad AS pk_codigo_ciudad,
        vm.nombre_ciudad
    FROM vm_codigos_postales vm
    WHERE vm.codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    AND vm.codigo_ciudad = p_codigo_ciudad::CHAR(2) -- Cast a CHAR
    ORDER BY vm.codigo_postal, vm.nombre_asentamiento
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_all_states
 * @description: Lista todos los estados, usado en /api/v2/estado.
 * @returns: Tabla con estructura StateRecord (CHAR para código).
 */
CREATE OR REPLACE FUNCTION get_all_states()
RETURNS TABLE (
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.pk_codigo_estado AS codigo_estado,
        e.nombre_estado
    FROM estados e
    ORDER BY e.nombre_estado;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_state_by_id
 * @description: Obtiene detalles de un estado, usado en /api/v2/estado/{estadoId}.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @returns: Tabla con estructura StateRecord (CHAR para código).
 */
CREATE OR REPLACE FUNCTION get_state_by_id(
    p_codigo_estado VARCHAR(2) -- Acepta VARCHAR
)
RETURNS TABLE (
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;

    RETURN QUERY
    SELECT
        e.pk_codigo_estado AS codigo_estado,
        e.nombre_estado
    FROM estados e
    WHERE e.pk_codigo_estado = p_codigo_estado::CHAR(2); -- Cast a CHAR
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_cities_by_state
 * @description: Lista ciudades por estado, usado en /api/v2/estado/{estadoId}/ciudad.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @returns: Tabla con estructura CityRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_cities_by_state(
    p_codigo_estado VARCHAR(2) -- Acepta VARCHAR
)
RETURNS TABLE (
    codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50),
    codigo_estado CHAR(2)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;

    RETURN QUERY
    SELECT
        c.pk_codigo_ciudad AS codigo_ciudad,
        c.nombre_ciudad,
        c.fk_codigo_estado AS codigo_estado
    FROM ciudades c
    WHERE c.fk_codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    ORDER BY c.nombre_ciudad;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_municipalities_by_state
 * @description: Lista municipios por estado, usado en /api/v2/estado/{estadoId}/municipios.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @returns: Tabla con estructura MunicipalityRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_municipalities_by_state(
    p_codigo_estado VARCHAR(2) -- Acepta VARCHAR
)
RETURNS TABLE (
    codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    codigo_estado CHAR(2)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;

    RETURN QUERY
    SELECT
        m.pk_codigo_municipio AS codigo_municipio,
        m.nombre_municipio,
        m.fk_codigo_estado AS codigo_estado
    FROM municipios m
    WHERE m.fk_codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    ORDER BY m.nombre_municipio;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_all_cities
 * @description: Lista todas las ciudades, usado en /api/v2/ciudad.
 * @returns: Tabla con estructura CityRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_all_cities()
RETURNS TABLE (
    codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50),
    codigo_estado CHAR(2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.pk_codigo_ciudad AS codigo_ciudad,
        c.nombre_ciudad,
        c.fk_codigo_estado AS codigo_estado
    FROM ciudades c
    ORDER BY c.nombre_ciudad;
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_city_by_id
 * @description: Obtiene detalles de una ciudad, usado en /api/v2/ciudad/{estadoId}/{ciudadId}.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @param p_codigo_ciudad: Código de la ciudad (2 dígitos).
 * @returns: Tabla con estructura CityRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_city_by_id(
    p_codigo_estado VARCHAR(2), -- Acepta VARCHAR
    p_codigo_ciudad VARCHAR(2) -- Acepta VARCHAR
)
RETURNS TABLE (
    codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50),
    codigo_estado CHAR(2)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;
    IF p_codigo_ciudad !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de ciudad debe ser de 2 dígitos';
    END IF;

    RETURN QUERY
    SELECT
        c.pk_codigo_ciudad AS codigo_ciudad,
        c.nombre_ciudad,
        c.fk_codigo_estado AS codigo_estado
    FROM ciudades c
    WHERE c.fk_codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    AND c.pk_codigo_ciudad = p_codigo_ciudad::CHAR(2); -- Cast a CHAR
END;
$$ LANGUAGE plpgsql;

/**
 * @function: get_settlements_by_city
 * @description: Lista asentamientos por ciudad con paginación, usado en /api/v2/ciudad/{estadoId}/{ciudadId}/colonias.
 * @param p_codigo_estado: Código del estado (2 dígitos).
 * @param p_codigo_ciudad: Código de la ciudad (2 dígitos).
 * @param p_limit: Límite de registros por página (1-100).
 * @param p_offset: Desplazamiento para paginación (>=0).
 * @returns: Tabla con estructura PostalCodeRecord (CHAR para códigos).
 */
CREATE OR REPLACE FUNCTION get_settlements_by_city(
    p_codigo_estado VARCHAR(2), -- Acepta VARCHAR
    p_codigo_ciudad VARCHAR(2), -- Acepta VARCHAR
    p_limit INTEGER,
    p_offset INTEGER
)
RETURNS TABLE (
    codigo_postal CHAR(5),
    nombre_asentamiento VARCHAR(100),
    tipo_asentamiento VARCHAR(50),
    zona VARCHAR(20),
    codigo_estado CHAR(2),
    nombre_estado VARCHAR(50),
    pk_codigo_municipio CHAR(3),
    nombre_municipio VARCHAR(50),
    pk_codigo_ciudad CHAR(2),
    nombre_ciudad VARCHAR(50)
) AS $$
BEGIN
    IF p_codigo_estado !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de estado debe ser de 2 dígitos';
    END IF;
    IF p_codigo_ciudad !~ '^[0-9]{2}$' THEN
        RAISE EXCEPTION 'El código de ciudad debe ser de 2 dígitos';
    END IF;
    IF p_limit < 1 OR p_limit > 100 THEN
        RAISE EXCEPTION 'El límite debe estar entre 1 y 100';
    END IF;
    IF p_offset < 0 THEN
        RAISE EXCEPTION 'El offset debe ser mayor o igual a 0';
    END IF;

    RETURN QUERY
    SELECT
        vm.codigo_postal,
        vm.nombre_asentamiento,
        vm.nombre_tipo_asentamiento AS tipo_asentamiento,
        vm.nombre_zona AS zona,
        vm.codigo_estado,
        vm.nombre_estado,
        vm.codigo_municipio AS pk_codigo_municipio,
        vm.nombre_municipio,
        vm.codigo_ciudad AS pk_codigo_ciudad,
        vm.nombre_ciudad
    FROM vm_codigos_postales vm
    WHERE vm.codigo_estado = p_codigo_estado::CHAR(2) -- Cast a CHAR
    AND vm.codigo_ciudad = p_codigo_ciudad::CHAR(2) -- Cast a CHAR
    ORDER BY vm.nombre_asentamiento
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
