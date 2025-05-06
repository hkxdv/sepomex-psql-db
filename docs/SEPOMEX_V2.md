# Especificaciones y Mejoras para la Base de Datos y API v2 - Proyecto SEPOMEX

Este documento consolida todas las especificaciones, cambios, y consideraciones para la versión optimizada (v2) de la base de datos y API del proyecto de códigos postales de México (SEPOMEX), desde el diseño inicial hasta la integración de la colección de Postman v2. Se detallan las optimizaciones realizadas, el análisis de los endpoints definidos en la colección v2, y las consideraciones para la API v2, asegurando un rendimiento óptimo para una base de datos estática con ~150,000 registros en `codigos_postales`. El diseño sigue un estándar personalizado basado en buenas prácticas de bases de datos, que incluye nomenclaturas claras (`pk_`, `fk_`), y normalización en Tercera Forma Normal (3FN).

## Resumen General

El proyecto SEPOMEX v2 optimiza la base de datos y API para consultas rápidas y escalables, soportando todos los endpoints definidos en la colección de Postman v2. Los principales objetivos fueron:

- **Optimización de la Base de Datos**: Reducir el tamaño, mejorar el rendimiento de consultas, y centralizar la lógica mediante funciones PL/pgSQL.
- **Soporte Completo de Endpoints v2**: Cubrir todas las rutas de la API v2 con funciones y controladores específicos.
- **Escalabilidad y Rendimiento**: Implementar índices, vistas materializadas, y potencialmente caching (ej. Redis) para tiempos de respuesta rápidos.
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

## Análisis de la Colección de Postman v2 (`SEPOMEX-API-v2.postman_collection.json`)

La colección de Postman v2 define la estructura esperada de la API REST que consume esta base de datos. A continuación se analizan los endpoints definidos y su correspondencia con las funciones PL/pgSQL:

> [!NOTE]
> Todos los endpoints de la v2 utilizan el prefijo `/api/v2/`. Las respuestas exitosas devuelven un objeto JSON con `success: true`, `message`, y `data` (que contiene el resultado como objeto o array de objetos).

### Endpoints de Códigos Postales (`/api/v2/postal/...`)

1.  **GET `/api/v2/postal/search`**

    - **Descripción:** Busca asentamientos por nombre.
    - **Parámetros:** `q` (query string), `limit` (int), `offset` (int).
    - **Función BD:** `search_settlements_by_name(p_query, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord (ej. `codigo_postal`, `nombre_asentamiento`, ..., `pk_codigo_municipio`, ..., `pk_codigo_ciudad`, ...).

2.  **GET `/api/v2/postal/codigo/{code}`**

    - **Descripción:** Busca todos los asentamientos para un código postal específico.
    - **Parámetros:** `{code}` (path param, 5 dígitos).
    - **Función BD:** `search_by_postal_code(p_codigo_postal)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

3.  **GET `/api/v2/postal/estado/{estadoId}`**

    - **Descripción:** Lista códigos postales/asentamientos por estado.
    - **Parámetros:** `{estadoId}` (path param, 2 dígitos), `limit` (int), `offset` (int).
    - **Función BD:** `get_postal_codes_by_state(p_codigo_estado, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

4.  **GET `/api/v2/postal/municipio/{estadoId}/{municipioId}`**

    - **Descripción:** Lista códigos postales/asentamientos por municipio.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos), `{municipioId}` (path, 3 dígitos), `limit` (int), `offset` (int).
    - **Función BD:** `get_postal_codes_by_municipality(p_codigo_estado, p_codigo_municipio, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

5.  **GET `/api/v2/postal/ciudad/{estadoId}/{ciudadId}`**
    - **Descripción:** Lista códigos postales/asentamientos por ciudad.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos), `{ciudadId}` (path, 2 dígitos), `limit` (int), `offset` (int).
    - **Función BD:** `get_postal_codes_by_city(p_codigo_estado, p_codigo_ciudad, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

### Endpoints de Estados (`/api/v2/estado/...`)

6.  **GET `/api/v2/estado`**

    - **Descripción:** Lista todos los estados.
    - **Parámetros:** Ninguno.
    - **Función BD:** `get_all_states()`.
    - **Respuesta (`data`):** Array de objetos con `codigo_estado`, `nombre_estado`.

7.  **GET `/api/v2/estado/{estadoId}`**

    - **Descripción:** Obtiene detalles de un estado específico.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos).
    - **Función BD:** `get_state_by_id(p_codigo_estado)`.
    - **Respuesta (`data`):** Objeto con `codigo_estado`, `nombre_estado`.

8.  **GET `/api/v2/estado/{estadoId}/cities`**

    - **Descripción:** Lista las ciudades de un estado específico.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos).
    - **Función BD:** `get_cities_by_state(p_codigo_estado)`.
    - **Respuesta (`data`):** Array de objetos con `codigo_ciudad`, `nombre_ciudad`, `codigo_estado`.

9.  **GET `/api/v2/estado/{estadoId}/municipios`**

    - **Descripción:** Lista los municipios de un estado específico.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos).
    - **Función BD:** `get_municipalities_by_state(p_codigo_estado)`.
    - **Respuesta (`data`):** Array de objetos con `codigo_municipio`, `nombre_municipio`, `codigo_estado`.

10. **GET `/api/v2/estado/{estadoId}/asentamientos`**
    - **Descripción:** Lista todos los asentamientos de un estado (similar a `/postal/estado/{estadoId}`).
    - **Parámetros:** `{estadoId}` (path, 2 dígitos), `limit` (int), `offset` (int).
    - **Función BD:** `get_postal_codes_by_state(p_codigo_estado, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

### Endpoints de Ciudades (`/api/v2/cities/...`)

11. **GET `/api/v2/cities`**

    - **Descripción:** Lista todas las ciudades a nivel nacional.
    - **Parámetros:** Ninguno.
    - **Función BD:** `get_all_cities()`.
    - **Respuesta (`data`):** Array de objetos con `codigo_ciudad`, `nombre_ciudad`, `codigo_estado`.

12. **GET `/api/v2/cities/{estadoId}/{ciudadId}`**

    - **Descripción:** Obtiene detalles de una ciudad específica.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos), `{ciudadId}` (path, 2 dígitos).
    - **Función BD:** `get_city_by_id(p_codigo_estado, p_codigo_ciudad)`.
    - **Respuesta (`data`):** Objeto con `codigo_ciudad`, `nombre_ciudad`, `codigo_estado`.

13. **GET `/api/v2/cities/{estadoId}/{ciudadId}/colonias`**

    - **Descripción:** Lista los asentamientos (colonias) de una ciudad específica.
    - **Parámetros:** `{estadoId}` (path, 2 dígitos), `{ciudadId}` (path, 2 dígitos), `limit` (int), `offset` (int).
    - **Función BD:** `get_settlements_by_city(p_codigo_estado, p_codigo_ciudad, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

14. **GET `/api/v2/cities/{estadoId}/{ciudadId}/codigos`**
    - **Descripción:** Lista los códigos postales asociados a una ciudad específica (similar a `/postal/ciudad/{estadoId}/{ciudadId}`).
    - **Parámetros:** `{estadoId}` (path, 2 dígitos), `{ciudadId}` (path, 2 dígitos), `limit` (int), `offset` (int).
    - **Función BD:** `get_postal_codes_by_city(p_codigo_estado, p_codigo_ciudad, p_limit, p_offset)`.
    - **Respuesta (`data`):** Array de objetos con estructura PostalCodeRecord.

### Observaciones del Análisis

- **Coherencia:** Existe una buena correspondencia entre los endpoints definidos en la colección v2 y las funciones PL/pgSQL implementadas en `database/functions.sql`.
- **Paginación:** Se aplica consistentemente (`limit`, `offset`) a los endpoints que pueden devolver listas largas de asentamientos/códigos postales.
- **Estructura de Respuesta:** Las funciones PL/pgSQL definen la estructura de datos retornada (PostalCodeRecord, StateRecord, CityRecord, MunicipalityRecord). La API debe mapear estos resultados al campo `data` de la respuesta JSON.
- **Rendimiento:** El uso de la vista materializada `vm_codigos_postales` y los índices adecuados en la BD, junto con las funciones PL/pgSQL, sienta las bases para una API de buen rendimiento. El caching a nivel de API (ej. Redis) sería un paso adicional para optimizar aún más.

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
    - `idx_codigos_postales_nombre_asentamiento_lower`: Para búsquedas `ILIKE` en `nombre_asentamiento`.
    - `idx_codigos_postales_codigo_postal`: Para búsquedas exactas por código postal.
    - `idx_codigos_postales_codigo_estado`: Para filtros por estado.
    - `idx_codigos_postales_codigo_municipio_not_null`, `idx_codigos_postales_codigo_ciudad_not_null`: Índices parciales para optimizar búsquedas cuando el municipio/ciudad no es nulo.
    - `idx_codigos_postales_codigo_tipo_asentamiento`, `idx_codigos_postales_id_zona`: Para posibles filtros adicionales.
  - Índices en `municipios` y `ciudades`:
    - `idx_municipios_codigo_estado`: Para listar municipios por estado.
    - `idx_ciudades_codigo_estado`: Para listar ciudades por estado.
  - Índices en `vm_codigos_postales`:
    - `idx_vm_codigos_postales_nombre_asentamiento_lower`, `idx_vm_codigos_postales_codigo_postal`, `idx_vm_codigos_postales_codigo_estado`, `idx_vm_codigos_postales_codigo_municipio`, `idx_vm_codigos_postales_codigo_ciudad`: Para acelerar consultas sobre la vista materializada.
- **Justificación**:
  - Evitan escaneos secuenciales costosos en `codigos_postales`.
  - Índices parciales optimizan consultas específicas.
  - Índices en tablas de catálogos (`municipios`, `ciudades`) y la vista materializada aceleran los joins precalculados y las consultas directas a la vista.

### 3. Vistas Materializadas (`database/views.sql`)

- **Cambios**:
  - `vm_codigos_postales` precomputa los joins entre `codigos_postales` y las tablas de catálogos (`estados`, `municipios`, `ciudades`, `tipos_asentamiento`, `zonas`).
  - La vista utiliza **alias** para las columnas de las tablas unidas (ej. `e.nombre_estado AS nombre_estado`, `m.pk_codigo_municipio AS codigo_municipio`). Esto simplifica las consultas que usan la vista.
  - Índices creados sobre la vista materializada para soportar patrones de consulta comunes (ver sección de Índices).
- **Justificación**:
  - Elimina la sobrecarga de realizar joins dinámicos en cada consulta, mejorando drásticamente el rendimiento para datos estáticos.
  - Simplifica las funciones PL/pgSQL que consultan datos combinados.

### 4. Funciones PL/pgSQL (`database/functions.sql`)

- **Cambios**:
  - Se implementaron funciones para encapsular la lógica de consulta para cada tipo de endpoint de la API v2.
  - Funciones de Búsqueda y Listado (consultan `vm_codigos_postales`):
    - `search_settlements_by_name(query, limit, offset)`
    - `search_by_postal_code(code)`
    - `get_postal_codes_by_state(state_code, limit, offset)`
    - `get_postal_codes_by_municipality(state_code, municipality_code, limit, offset)`
    - `get_postal_codes_by_city(state_code, city_code, limit, offset)`
    - `get_settlements_by_city(state_code, city_code, limit, offset)`
  - Funciones de Catálogo (consultan tablas `estados`, `municipios`, `ciudades`):
    - `get_all_states()`
    - `get_state_by_id(state_code)`
    - `get_cities_by_state(state_code)`
    - `get_municipalities_by_state(state_code)`
    - `get_all_cities()`
    - `get_city_by_id(state_code, city_code)`
  - Implementan validaciones básicas de parámetros y paginación (`limit`, `offset`) donde aplica.
  - Definen explícitamente la estructura de retorno (`RETURNS TABLE (...)`) usando los tipos de datos correctos (`CHAR`, `VARCHAR`, etc.) consistentes con el esquema y la vista.
- **Justificación**:
  - Centralizan la lógica de acceso a datos, facilitando el mantenimiento y la consistencia.
  - Optimizan las consultas utilizando la vista materializada e índices.
  - Proveen una interfaz clara y segura para la capa de aplicación (API).
  - La paginación previene la sobrecarga al devolver grandes conjuntos de resultados.

## Consideraciones Adicionales sobre los Datos

### "Duplicidad Funcional" en los Datos Fuente

Durante las pruebas y el análisis de los datos consultados mediante las funciones PL/pgSQL (ej. `search_by_postal_code`), se observó que para ciertos criterios (como un código postal específico o un nombre de asentamiento común), podían devolverse múltiples filas que parecían idénticas en sus campos descriptivos (nombre de asentamiento, tipo, zona, nombres geográficos).

**Análisis:** Una investigación más profunda, consultando directamente la tabla `codigos_postales` y examinando la clave primaria `pk_id_codigo_postal`, reveló que estas filas **no son duplicados reales** en la base de datos. Cada fila tiene un `pk_id_codigo_postal` único, indicando que representan entradas distintas tal como existen en el archivo fuente original de SEPOMEX. Esta "duplicidad funcional" es, por tanto, una característica inherente a cómo SEPOMEX estructura o registra sus datos.

**Decisión de Diseño y Manejo:**

1.  **Base de Datos (Fuente de Verdad):** Se decidió mantener todos estos registros distintos en la base de datos (`codigos_postales`). Esto asegura la máxima fidelidad a los datos originales y preserva la granularidad que podría ser útil para futuros análisis o auditorías. Las funciones PL/pgSQL continuarán devolviendo _todos_ los registros que coincidan con los criterios de búsqueda.

2.  **Capa de API (Lógica de Presentación):** La responsabilidad de presentar los datos de una manera "limpia" o deduplicada recae en la capa de la API (los controladores). Si para un endpoint específico, múltiples registros devueltos por la base de datos son funcionalmente idénticos _desde la perspectiva del consumidor de la API_ (es decir, tienen los mismos valores en los campos expuestos por la API), el controlador de la API debe implementar la lógica para filtrar o agrupar estos resultados antes de enviarlos en la respuesta JSON. Esto asegura que el consumidor reciba datos concisos y sin redundancia aparente, manteniendo al mismo tiempo la integridad de los datos completos en la base de datos.

## Historial de Refinamiento y Correcciones

Durante el desarrollo, implementación y prueba de la v2, se identificaron y corrigieron varios problemas técnicos:

**Errores de Codificación (UTF-8):** Al importar los archivos SQL generados por el script Python en `psql`, surgieron errores relacionados con caracteres inválidos (ej. `ERROR: carácter con secuencia de bytes 0x81 en la codificación «UTF8» no es válido`). Esto se solucionó refinando la función `clean_text` en `src/utils.py` para manejar y eliminar caracteres problemáticos (incluyendo controles C1) durante la lectura del archivo TXT original, y asegurando la codificación correcta al escribir los archivos SQL.
