-- Consultas de verificación para la base de datos SEPOMEX v2

-- 1. Totales generales en catálogos
SELECT 'estados' as tabla, COUNT(*) as total FROM estados
UNION ALL
SELECT 'municipios', COUNT(*) FROM municipios
UNION ALL
SELECT 'ciudades', COUNT(*) FROM ciudades
UNION ALL
SELECT 'tipos_asentamiento', COUNT(*) FROM tipos_asentamiento
UNION ALL
SELECT 'zonas', COUNT(*) FROM zonas;

-- 2. Total general en tabla principal
SELECT COUNT(*) as total_registros_cp FROM codigos_postales;

-- 3. Distribución por zona en codigos_postales
SELECT
    z.nombre_zona,
    COUNT(cp.pk_id_codigo_postal) as cantidad,
    ROUND(COUNT(cp.pk_id_codigo_postal) * 100.0 / SUM(COUNT(cp.pk_id_codigo_postal)) OVER (), 2) as porcentaje
FROM codigos_postales cp
JOIN zonas z ON cp.fk_id_zona = z.pk_id_zona
GROUP BY z.nombre_zona
ORDER BY cantidad DESC;

-- 4. Top 10 estados con más códigos postales (registros en tabla principal)
SELECT
    e.nombre_estado,
    COUNT(cp.pk_id_codigo_postal) as cantidad,
    ROUND(COUNT(cp.pk_id_codigo_postal) * 100.0 / SUM(COUNT(cp.pk_id_codigo_postal)) OVER (), 2) as porcentaje
FROM codigos_postales cp
JOIN estados e ON cp.fk_codigo_estado = e.pk_codigo_estado
GROUP BY e.nombre_estado
ORDER BY cantidad DESC
LIMIT 10;

-- 5. Distribución por tipo de asentamiento en codigos_postales
SELECT
    ta.nombre_tipo_asentamiento,
    COUNT(cp.pk_id_codigo_postal) as cantidad,
    ROUND(COUNT(cp.pk_id_codigo_postal) * 100.0 / SUM(COUNT(cp.pk_id_codigo_postal)) OVER (), 2) as porcentaje
FROM codigos_postales cp
JOIN tipos_asentamiento ta ON cp.fk_codigo_tipo_asentamiento = ta.pk_codigo_tipo_asentamiento
GROUP BY ta.nombre_tipo_asentamiento
ORDER BY cantidad DESC;

-- 6. Verificar registros de códigos postales sin municipio o sin ciudad (NULL permitido)
SELECT
    'Registros CP sin municipio' as descripcion,
    COUNT(*) as cantidad,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM codigos_postales), 2) as porcentaje
FROM codigos_postales
WHERE fk_codigo_municipio IS NULL
UNION ALL
SELECT
    'Registros CP sin ciudad',
    COUNT(*),
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM codigos_postales), 2)
FROM codigos_postales
WHERE fk_codigo_ciudad IS NULL;

-- 7. Top 10 municipios con más registros en codigos_postales
SELECT
    m.nombre_municipio,
    e.nombre_estado,
    COUNT(cp.pk_id_codigo_postal) as cantidad
FROM codigos_postales cp
JOIN municipios m ON cp.fk_codigo_municipio = m.pk_codigo_municipio AND cp.fk_codigo_estado = m.fk_codigo_estado
JOIN estados e ON cp.fk_codigo_estado = e.pk_codigo_estado
GROUP BY m.nombre_municipio, e.nombre_estado
ORDER BY cantidad DESC
LIMIT 10;

-- 8. Verificar integridad referencial (FKs requeridas)
-- (Nota: Estas deberían dar 0 si las FKs se aplicaron correctamente y los datos son válidos)
SELECT
    'CP con fk_codigo_estado inválido' as problema,
    COUNT(*) as cantidad
FROM codigos_postales cp
LEFT JOIN estados e ON cp.fk_codigo_estado = e.pk_codigo_estado
WHERE e.pk_codigo_estado IS NULL
UNION ALL
SELECT
    'CP con fk_codigo_tipo_asentamiento inválido',
    COUNT(*)
FROM codigos_postales cp
LEFT JOIN tipos_asentamiento ta ON cp.fk_codigo_tipo_asentamiento = ta.pk_codigo_tipo_asentamiento
WHERE ta.pk_codigo_tipo_asentamiento IS NULL
UNION ALL
SELECT
    'CP con fk_id_zona inválido',
    COUNT(*)
FROM codigos_postales cp
LEFT JOIN zonas z ON cp.fk_id_zona = z.pk_id_zona
WHERE z.pk_id_zona IS NULL
UNION ALL
-- Chequeo opcional para FKs nulleables (debería dar 0 si los códigos existen cuando no son null)
SELECT
    'CP con fk_codigo_municipio inválido (cuando no es NULL)',
    COUNT(*)
FROM codigos_postales cp
LEFT JOIN municipios m ON cp.fk_codigo_municipio = m.pk_codigo_municipio AND cp.fk_codigo_estado = m.fk_codigo_estado
WHERE cp.fk_codigo_municipio IS NOT NULL AND m.pk_codigo_municipio IS NULL
UNION ALL
SELECT
    'CP con fk_codigo_ciudad inválido (cuando no es NULL)',
    COUNT(*)
FROM codigos_postales cp
LEFT JOIN ciudades c ON cp.fk_codigo_ciudad = c.pk_codigo_ciudad AND cp.fk_codigo_estado = c.fk_codigo_estado
WHERE cp.fk_codigo_ciudad IS NOT NULL AND c.pk_codigo_ciudad IS NULL; 