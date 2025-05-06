-- Consultas detalladas de ejemplo para la base de datos SEPOMEX v2
-- Usando las funciones PL/pgSQL optimizadas

-- Ejemplo 1: Buscar asentamientos por nombre ('Centro') con paginación (limite 10, offset 0)
-- Llama a: search_settlements_by_name(p_query VARCHAR(100), p_limit INTEGER, p_offset INTEGER)
SELECT * FROM search_settlements_by_name('Centro', 10, 0);

-- Ejemplo 2: Buscar todos los asentamientos para un código postal específico ('01000')
-- Llama a: search_by_postal_code(p_codigo_postal VARCHAR(5))
SELECT * FROM search_by_postal_code('01000');

-- Ejemplo 3: Obtener los primeros 5 códigos postales del estado '09' (Ciudad de México)
-- Llama a: get_postal_codes_by_state(p_codigo_estado VARCHAR(2), p_limit INTEGER, p_offset INTEGER)
SELECT * FROM get_postal_codes_by_state('09', 5, 0);

-- Ejemplo 4: Obtener los siguientes 5 códigos postales del estado '09' (paginación)
-- Llama a: get_postal_codes_by_state(p_codigo_estado VARCHAR(2), p_limit INTEGER, p_offset INTEGER)
SELECT * FROM get_postal_codes_by_state('09', 5, 5);

-- Ejemplo 5: Obtener los primeros 10 códigos postales del municipio '010' (Álvaro Obregón) en el estado '09' (CDMX)
-- Llama a: get_postal_codes_by_municipality(p_codigo_estado VARCHAR(2), p_codigo_municipio VARCHAR(3), p_limit INTEGER, p_offset INTEGER)
SELECT * FROM get_postal_codes_by_municipality('09', '010', 10, 0);

-- Ejemplo 6: Obtener los primeros 3 códigos postales de la ciudad '01' (Ciudad de México) en el estado '09' (CDMX)
-- Nota: En CDMX, la ciudad puede no ser tan relevante como en otros estados.
-- Llama a: get_postal_codes_by_city(p_codigo_estado VARCHAR(2), p_codigo_ciudad VARCHAR(2), p_limit INTEGER, p_offset INTEGER)
SELECT * FROM get_postal_codes_by_city('09', '01', 3, 0);

-- Ejemplo 7: Listar todos los estados
-- Llama a: get_all_states()
SELECT * FROM get_all_states();

-- Ejemplo 8: Obtener detalles del estado '19' (Nuevo León)
-- Llama a: get_state_by_id(p_codigo_estado VARCHAR(2))
SELECT * FROM get_state_by_id('19');

-- Ejemplo 9: Listar todas las ciudades del estado '19' (Nuevo León)
-- Llama a: get_cities_by_state(p_codigo_estado VARCHAR(2))
SELECT * FROM get_cities_by_state('19');

-- Ejemplo 10: Listar todos los municipios del estado '19' (Nuevo León)
-- Llama a: get_municipalities_by_state(p_codigo_estado VARCHAR(2))
SELECT * FROM get_municipalities_by_state('19');

-- Ejemplo 11: Listar todas las ciudades (a nivel nacional)
-- Llama a: get_all_cities()
SELECT * FROM get_all_cities();

-- Ejemplo 12: Obtener detalles de la ciudad '01' (Guadalajara) en el estado '14' (Jalisco)
-- Llama a: get_city_by_id(p_codigo_estado VARCHAR(2), p_codigo_ciudad VARCHAR(2))
SELECT * FROM get_city_by_id('14', '01');

-- Ejemplo 13: Listar los primeros 5 asentamientos de la ciudad '01' (Guadalajara) en el estado '14' (Jalisco)
-- Llama a: get_settlements_by_city(p_codigo_estado VARCHAR(2), p_codigo_ciudad VARCHAR(2), p_limit INTEGER, p_offset INTEGER)
SELECT * FROM get_settlements_by_city('14', '01', 5, 0);


-- Consulta directa a la vista materializada (ejemplo, no recomendado para API)
-- Muestra los primeros 50 registros de la vista completa.
SELECT
    vm.codigo_postal,
    vm.nombre_asentamiento,
    vm.nombre_tipo_asentamiento AS tipo_asentamiento,
    vm.nombre_zona AS zona,
    vm.codigo_estado,
    vm.nombre_estado,
    vm.codigo_municipio,
    vm.nombre_municipio,
    vm.codigo_ciudad,
    vm.nombre_ciudad
FROM vm_codigos_postales vm
ORDER BY vm.codigo_estado, vm.codigo_municipio, vm.codigo_postal, vm.nombre_asentamiento
LIMIT 50; 