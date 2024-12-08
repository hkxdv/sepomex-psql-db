-- Consultas de verificación para la base de datos SEPOMEX

-- 1. Totales generales
SELECT COUNT(*) as total_registros FROM codigos_postales;

-- 2. Distribución por zona
SELECT 
    z.tipo_zona, 
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
FROM codigos_postales cp
JOIN zonas z ON cp.id_zona = z.id_zona
GROUP BY z.tipo_zona
ORDER BY cantidad DESC;

-- 3. Top 10 estados con más códigos postales
SELECT 
    e.nombre_estado, 
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
FROM codigos_postales cp
JOIN estados e ON cp.codigo_estado = e.codigo_estado
GROUP BY e.nombre_estado
ORDER BY cantidad DESC
LIMIT 10;

-- 4. Distribución por tipo de asentamiento
SELECT 
    ta.nombre_tipo_asentamiento,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
FROM codigos_postales cp
JOIN tipos_asentamiento ta ON cp.codigo_tipo_asentamiento = ta.codigo_tipo_asentamiento
GROUP BY ta.nombre_tipo_asentamiento
ORDER BY cantidad DESC;

-- 5. Verificar registros sin ciudad
SELECT 
    COUNT(*) as total_sin_ciudad,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as porcentaje
FROM codigos_postales
WHERE codigo_ciudad IS NULL;

-- 6. Top 10 ciudades con más códigos postales
SELECT 
    c.nombre_ciudad,
    e.nombre_estado,
    COUNT(*) as cantidad
FROM codigos_postales cp
JOIN ciudades c ON cp.codigo_ciudad = c.codigo_ciudad 
    AND cp.codigo_estado = c.codigo_estado
JOIN estados e ON cp.codigo_estado = e.codigo_estado
GROUP BY c.nombre_ciudad, e.nombre_estado
ORDER BY cantidad DESC
LIMIT 10;

-- 7. Códigos postales por municipio (top 10)
SELECT 
    m.nombre_municipio,
    e.nombre_estado,
    COUNT(*) as cantidad
FROM codigos_postales cp
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio 
    AND cp.codigo_estado = m.codigo_estado
JOIN estados e ON cp.codigo_estado = e.codigo_estado
GROUP BY m.nombre_municipio, e.nombre_estado
ORDER BY cantidad DESC
LIMIT 10;

-- 8. Verificar integridad de datos
SELECT 
    'Códigos postales sin estado' as descripcion, COUNT(*) as cantidad
FROM codigos_postales WHERE codigo_estado IS NULL
UNION ALL
SELECT 
    'Códigos postales sin municipio', COUNT(*)
FROM codigos_postales WHERE codigo_municipio IS NULL
UNION ALL
SELECT 
    'Códigos postales sin tipo de asentamiento', COUNT(*)
FROM codigos_postales WHERE codigo_tipo_asentamiento IS NULL
UNION ALL
SELECT 
    'Códigos postales sin zona', COUNT(*)
FROM codigos_postales WHERE id_zona IS NULL; 
