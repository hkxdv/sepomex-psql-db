-- 1. Buscar por código postal (detalle completo)
SELECT 
    cp.codigo_postal,
    cp.nombre_asentamiento,
    e.nombre_estado,
    m.nombre_municipio,
    COALESCE(c.nombre_ciudad, 'Sin Ciudad') as nombre_ciudad,
    ta.nombre_tipo_asentamiento,
    z.tipo_zona,
    cp.codigo_postal_administracion,
    cp.codigo_oficina_postal,
    cp.id_asentamiento_consecutivo
FROM codigos_postales cp
JOIN estados e ON cp.codigo_estado = e.codigo_estado
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio 
    AND cp.codigo_estado = m.codigo_estado
LEFT JOIN ciudades c ON cp.codigo_ciudad = c.codigo_ciudad 
    AND cp.codigo_estado = c.codigo_estado
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
JOIN zonas z ON cp.id_zona = z.id_zona
WHERE cp.codigo_postal = :codigo_postal;

-- 2. Buscar por nombre de asentamiento (búsqueda parcial)
SELECT 
    cp.codigo_postal,
    cp.nombre_asentamiento,
    e.nombre_estado,
    m.nombre_municipio,
    ta.nombre_tipo_asentamiento,
    z.tipo_zona
FROM codigos_postales cp
JOIN estados e ON cp.codigo_estado = e.codigo_estado
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio 
    AND cp.codigo_estado = m.codigo_estado
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
JOIN zonas z ON cp.id_zona = z.id_zona
WHERE cp.nombre_asentamiento ILIKE '%' || :nombre_asentamiento || '%'
ORDER BY e.nombre_estado, m.nombre_municipio, cp.nombre_asentamiento;

-- 3. Todos los códigos postales de un municipio
SELECT 
    cp.codigo_postal,
    cp.nombre_asentamiento,
    ta.nombre_tipo_asentamiento,
    z.tipo_zona,
    COALESCE(c.nombre_ciudad, 'Sin Ciudad') as nombre_ciudad
FROM codigos_postales cp
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
JOIN zonas z ON cp.id_zona = z.id_zona
LEFT JOIN ciudades c ON cp.codigo_ciudad = c.codigo_ciudad 
    AND cp.codigo_estado = c.codigo_estado
WHERE cp.codigo_estado = :codigo_estado 
    AND cp.codigo_municipio = :codigo_municipio
ORDER BY cp.codigo_postal;

-- 4. Códigos postales por tipo de asentamiento en un estado
SELECT 
    cp.codigo_postal,
    cp.nombre_asentamiento,
    m.nombre_municipio,
    z.tipo_zona,
    cp.codigo_postal_administracion
FROM codigos_postales cp
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio 
    AND cp.codigo_estado = m.codigo_estado
JOIN zonas z ON cp.id_zona = z.id_zona
WHERE cp.codigo_estado = :codigo_estado 
    AND cp.codigo_tipo_asentamiento = :codigo_tipo_asentamiento
ORDER BY m.nombre_municipio, cp.nombre_asentamiento;

-- 5. Búsqueda por rango de códigos postales
SELECT 
    cp.codigo_postal,
    cp.nombre_asentamiento,
    e.nombre_estado,
    m.nombre_municipio,
    ta.nombre_tipo_asentamiento,
    z.tipo_zona
FROM codigos_postales cp
JOIN estados e ON cp.codigo_estado = e.codigo_estado
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio 
    AND cp.codigo_estado = m.codigo_estado
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
JOIN zonas z ON cp.id_zona = z.id_zona
WHERE cp.codigo_postal BETWEEN :codigo_postal_inicio AND :codigo_postal_fin
ORDER BY cp.codigo_postal;

-- 6. Códigos postales por zona en una ciudad
SELECT 
    cp.codigo_postal,
    cp.nombre_asentamiento,
    ta.nombre_tipo_asentamiento,
    cp.codigo_postal_administracion
FROM codigos_postales cp
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
WHERE cp.codigo_estado = :codigo_estado 
    AND cp.codigo_ciudad = :codigo_ciudad
    AND cp.id_zona = :id_zona
ORDER BY cp.codigo_postal;

-- 7. Resumen de asentamientos por código postal
SELECT 
    cp.codigo_postal,
    e.nombre_estado,
    m.nombre_municipio,
    COUNT(*) as total_asentamientos,
    STRING_AGG(DISTINCT z.tipo_zona, ', ') as tipos_zona,
    STRING_AGG(DISTINCT ta.nombre_tipo_asentamiento, ', ') as tipos_asentamiento
FROM codigos_postales cp
JOIN estados e ON cp.codigo_estado = e.codigo_estado
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio 
    AND cp.codigo_estado = m.codigo_estado
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
JOIN zonas z ON cp.id_zona = z.id_zona
WHERE cp.codigo_postal = :codigo_postal
GROUP BY cp.codigo_postal, e.nombre_estado, m.nombre_municipio; 