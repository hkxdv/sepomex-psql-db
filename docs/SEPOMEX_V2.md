# Especificaciones y Mejoras para la Base de Datos y API v2 - Proyecto SEPOMEX

Este documento consolida todas las especificaciones, cambios, y consideraciones para la versión optimizada (v2) de la base de datos y API del proyecto de códigos postales de México (SEPOMEX), desde el diseño inicial hasta la integración de la colección de Postman. Se detallan las optimizaciones realizadas, el análisis de los endpoints, y las consideraciones para la API v2, asegurando un rendimiento óptimo para una base de datos estática con ~150,000 registros en `codigos_postales`. El diseño sigue un estándar personalizado basado en buenas prácticas de bases de datos, que incluye nomenclaturas claras (`pk_`, `fk_`), y normalización en Tercera Forma Normal (3FN).

## Resumen General

El proyecto SEPOMEX v2 optimiza la base de datos y API para consultas rápidas y escalables, soportando todos los endpoints definidos en la colección de Postman. Los principales objetivos fueron:

- **Optimización de la Base de Datos**: Reducir el tamaño, mejorar el rendimiento de consultas, y centralizar la lógica mediante funciones PL/pgSQL.
- **Soporte Completo de Endpoints**: Cubrir todas las rutas de la API con funciones y controladores específicos.
- **Escalabilidad y Rendimiento**: Implementar índices, vistas materializadas, y Redis caching para tiempos de respuesta <100ms.
- **Mantenibilidad**: Documentación clara, estructura modular, y convenciones consistentes.

## Configuración General

- **Nomenclatura**: Prefijos `pk_` (claves primarias) y `fk_` (claves foráneas), siguiendo un estándar personalizado de buenas prácticas.
- **Normalización**: Estructura en 3FN, eliminando redundancias y asegurando dependencia exclusiva de claves primarias.
- **Documentación**: Con anotaciones `@table`, `@index`, `@view`, `@function` para todos los objetos de la base de datos.

## Evolución del Diseño

### Fase Inicial: Diseño de la Base de Datos

El diseño inicial definió las tablas (`estados`, `municipios`, `ciudades`, `tipos_asentamiento`, `zonas`, `codigos_postales`) siguiendo un estándar personalizado basado en buenas prácticas:

- **Campos Iniciales**: Incluyó `hora`, `fecha`, y `estado` en todas las tablas para auditoría.
- **Tipos de Datos**: Uso de `VARCHAR(100)` para nombres y `SERIAL` para identificadores.
- **Columnas Adicionales**: Incluyó `codigo_postal_administracion`, `codigo_oficina_postal`, e `id_asentamiento_consecutivo` en `codigos_postales`.

### Primera Iteración: Optimización

Se optimizó la estructura para reducir el tamaño y mejorar el rendimiento:

- **Tipos de Datos**:
  - Reducción de `VARCHAR(100)` a `VARCHAR(50)` para `nombre_estado`, `nombre_municipio`, y `nombre_ciudad` (nombres más largos ~30 caracteres).
  - Cambio de `pk_id_zona` y `fk_id_zona` a `SMALLINT` (2 bytes) en lugar de `SERIAL` (4 bytes), dado que `zonas` tiene ~3-5 registros.
- **Índices**:
  - Creados para consultas frecuentes (`nombre_asentamiento`, `codigo_postal`, `fk_codigo_estado`, etc.).
  - Índices parciales para `fk_codigo_municipio` y `fk_codigo_ciudad` cuando no son `NULL`.
- **Vista Materializada**:
  - `vm_codigos_postales` para precomputar joins.
- **Funciones PL/pgSQL**:
  - `search_settlements_by_name` y `search_by_postal_code` con paginación.
- **Eliminación de Columnas**:
  - `codigo_postal_administracion`, `codigo_oficina_postal`, e `id_asentamiento_consecutivo` eliminados de `codigos_postales`.

### Segunda Iteración: Eliminación de Columnas Redundantes

Confirmado que `hora`, `fecha`, y `estado` no eran necesarios en una base de datos estática, se eliminaron:

- **Impacto**: Ahorro de ~3.6 MB en `codigos_postales` (~150,000 x 24 bytes).
- **Archivos Afectados**: Solo `sepomex_schema.sql`.

### Tercera Iteración: Incorporación de la Colección de Postman

La colección de Postman (`SEPOMEX-API.postman_collection.json`) definió 14 endpoints, permitiendo un análisis detallado:

- **Soporte Completo**: Nuevas funciones PL/pgSQL y controladores para todas las rutas.
- **Índices Adicionales**: Para `municipios` y `ciudades`.
- **Redis Caching**: Integrado en todos los controladores.

## Análisis de la Colección de Postman

La colección organiza los endpoints en tres grupos: **Códigos Postales**, **Estados**, y **Ciudades**. A continuación, un resumen:

### Endpoints de Códigos Postales

1. **GET /api/v1/postal/search?q={q}**

   - Busca asentamientos por nombre (ej. `q=centro`).
   - Patrón: `ILIKE` en `nombre_asentamiento` con joins.
   - Soporte: `search_settlements_by_name`.

2. **GET /api/v1/postal/codigo/{code}**

   - Busca por código postal exacto (ej. `29000`).
   - Patrón: Filtro en `codigo_postal`.
   - Soporte: `search_by_postal_code`.

3. **GET /api/v1/postal/estado/{estadoId}**

   - Lista códigos postales por estado (ej. `07`).
   - Patrón: Filtro en `fk_codigo_estado`.

4. **GET /api/v1/postal/municipio/{estadoId}/{municipioId}**

   - Lista códigos postales por municipio (ej. `07/001`).
   - Patrón: Filtro en `fk_codigo_estado` y `fk_codigo_municipio`.

5. **GET /api/v1/postal/ciudad/{estadoId}/{ciudadId}**
   - Lista códigos postales por ciudad (ej. `09/01`).
   - Patrón: Filtro en `fk_codigo_estado` y `fk_codigo_ciudad`.

### Endpoints de Estados

6. **GET /api/v1/estado**

   - Lista todos los estados (~32 registros).
   - Patrón: `SELECT` desde `estados`.

7. **GET /api/v1/estado/{estadoId}**

   - Detalles de un estado (ej. `09`).
   - Patrón: Filtro en `pk_codigo_estado`.

8. **GET /api/v1/estado/{estadoId}/ciudad**

   - Lista ciudades por estado (ej. `07`).
   - Patrón: Filtro en `fk_codigo_estado` en `ciudades`.

9. **GET /api/v1/estado/{estadoId}/municipios**

   - Lista municipios por estado (ej. `07`).
   - Patrón: Filtro en `fk_codigo_estado` en `municipios`.

10. **GET /api/v1/estado/{estadoId}/asentamientos**
    - Lista asentamientos por estado (ej. `07`).
    - Patrón: Filtro en `fk_codigo_estado` en `codigos_postales`.

### Endpoints de Ciudades

11. **GET /api/v1/ciudad**

    - Lista todas las ciudades (~500 registros).
    - Patrón: `SELECT` desde `ciudades`.

12. **GET /api/v1/ciudad/{estadoId}/{ciudadId}**

    - Detalles de una ciudad (ej. `07/01`).
    - Patrón: Filtro en `fk_codigo_estado` y `pk_codigo_ciudad`.

13. **GET /api/v1/ciudad/{estadoId}/{ciudadId}/colonias**

    - Lista asentamientos por ciudad (ej. `07/01`).
    - Patrón: Filtro en `fk_codigo_estado` y `fk_codigo_ciudad` en `codigos_postales`.

14. **GET /api/v1/ciudad/{estadoId}/{ciudadId}/codigos**
    - Lista códigos postales por ciudad (ej. `07/01`).
    - Patrón: Similar a `/postal/ciudad/{estadoId}/{ciudadId}`.

### Observaciones

- **Patrones Comunes**: Filtros en `codigos_postales` por `fk_codigo_estado`, `fk_codigo_municipio`, `fk_codigo_ciudad`, o `nombre_asentamiento`, con joins frecuentes.
- **Paginación**: Asumida para listas (ej. `/search`, `/estado/{estadoId}`) con `limit` y `offset`.
- **Caching**: Ideal para `/search`, `/codigo/{code}`, y catálogos (`/estado`, `/ciudad`).
- **Respuesta Asumida**: Incluye `codigo_postal`, `nombre_asentamiento`, `tipo_asentamiento`, `zona`, `nombre_estado`, `nombre_municipio`, `nombre_ciudad`.

## Cambios Realizados en la Base de Datos

### 1. Estructura de Tablas (`database/schema.sql`)

- **Cambios**:
  - Eliminadas columnas redundantes:
    - `hora`, `fecha`, `estado` (~3.6 MB ahorrados en `codigos_postales`).
    - `codigo_postal_administracion`, `codigo_oficina_postal`, `id_asentamiento_consecutivo` (~2.1 MB ahorrados).
  - Optimización de tipos de datos:
    - `VARCHAR(50)` para `nombre_estado`, `nombre_municipio`, `nombre_ciudad`.
    - `SMALLINT` para `pk_id_zona` y `fk_id_zona` (~300 KB ahorrados).
  - Restricciones:
    - `NOT NULL` en `fk_codigo_estado`, `fk_codigo_tipo_asentamiento`, `fk_id_zona`.
    - `NULL` permitido en `fk_codigo_municipio` y `fk_codigo_ciudad`.
    - `CHECK` para formatos (ej. `codigo_postal ~ '^[0-9]{5}$'`).
  - Almacenamiento: `FILLFACTOR = 90`.
- **Justificación**:
  - Reducción de tamaño mejora escaneos y joins.
  - Restricciones aseguran integridad.
  - Eliminación de columnas simplifica la estructura.

### 2. Índices (`database/indexes.sql`)

- **Cambios**:
  - Índices en `codigos_postales`:
    - `idx_codigos_postales_nombre_asentamiento_lower`: Para `/search`.
    - `idx_codigos_postales_codigo_postal`: Para `/codigo/{code}`.
    - `idx_codigos_postales_codigo_estado`: Para filtros por estado.
    - `idx_codigos_postales_codigo_municipio_not_null`, `idx_codigos_postales_codigo_ciudad_not_null`: Índices parciales.
    - `idx_codigos_postales_codigo_tipo_asentamiento`, `idx_codigos_postales_id_zona`: Filtros secundarios.
  - Nuevos índices:
    - `idx_municipios_codigo_estado`: Para `/estado/{estadoId}/municipios`.
    - `idx_ciudades_codigo_estado`: Para `/estado/{estadoId}/ciudad`.
- **Justificación**:
  - Evitan escaneos secuenciales en `codigos_postales` (~150,000 filas).
  - Índices parciales optimizan consultas específicas.
  - Nuevos índices aceleran catálogos (~2,500 municipios, ~500 ciudades).

### 3. Vistas Materializadas (`database/views.sql`)

- **Cambios**:
  - `vm_codigos_postales` precomputa joins.
  - Ajustada para usar `pk_codigo_municipio` y `pk_codigo_ciudad`.
  - Índices: `idx_vm_codigos_postales_nombre_asentamiento_lower`, `idx_vm_codigos_postales_codigo_postal`, `idx_vm_codigos_postales_codigo_estado`.
- **Justificación**:
  - Elimina sobrecarga de joins dinámicos.
  - Índices soportan patrones de consulta.
  - Ideal para datos estáticos.

### 4. Funciones PL/pgSQL (`database/functions.sql`)

- **Cambios**:
  - Actualizadas:
    - `search_settlements_by_name`: Búsqueda por nombre con paginación.
    - `search_by_postal_code`: Búsqueda por código postal.
  - Nuevas:
    - `get_postal_codes_by_state`, `get_postal_codes_by_municipality`, `get_postal_codes_by_city`.
    - `get_cities_by_state`, `get_municipalities_by_state`, `get_state_by_id`, `get_city_by_id`, `get_all_states`, `get_all_cities`.
  - Paginación en funciones basadas en `codigos_postales`.
- **Justificación**:
  - Centralizan lógica, facilitando mantenimiento.
  - Paginación asegura escalabilidad.
  - Estructura tabular simplifica integración.
