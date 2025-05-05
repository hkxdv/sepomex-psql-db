# Resumen de Cambios del Proyecto SEPOMEX-PSQL-DB (v1 a v2)

Este documento resume las principales modificaciones realizadas en el proyecto, evolucionando desde una estructura inicial hacia una versión 2 más organizada, modular y optimizada.

## 1. Estructura del Proyecto

La estructura general del proyecto fue reorganizada significativamente para mejorar la claridad y separación de responsabilidades:

-   **`src/`**: Nuevo directorio que contiene todo el código fuente refactorizado del script Python para generar los archivos SQL v2.
-   **`database/`**: (Renombrado desde `database_v2/`) Directorio que agrupa todos los archivos SQL relacionados con la definición de la base de datos v2 (`schema.sql`, `functions.sql`, `indexes.sql`, `views.sql`).
-   **`data/`**: Reorganizado internamente:
    -   `data/input/`: Contiene el archivo de datos fuente (`sepomex_data.txt`).
    -   `data/generated_sql_v2/`: Directorio específico para los archivos SQL generados por el script v2.
-   **`docs/`**: Nuevo directorio para centralizar toda la documentación del proyecto (README, especificaciones v2, prompts, etc.).
-   **`queries/`**: (Renombrado desde `queries_v2/`) Nuevo directorio que contiene consultas SQL de ejemplo y de prueba para la versión 2 de la base de datos.
-   **`legacy_v1/`**: Nuevo directorio que archiva todo el código y los artefactos de la versión 1 (script Python original, schema v1, datos generados v1, queries v1).
-   **Archivos Raíz**: Se añadieron archivos estándar de configuración y gestión de proyectos Python (`requirements.txt`, `.gitignore`, `pyproject.toml`). Se actualizó `README.md`.

## 2. Base de Datos (v2)

La definición de la base de datos fue optimizada y formalizada:

-   **Schema (`database/schema.sql`)**: 
    -   Se adoptó la nomenclatura `pk_` / `fk_`.
    -   Se optimizaron tipos de datos (`VARCHAR(50)`, `SMALLINT`).
    -   Se eliminaron columnas redundantes de v1 (`hora`, `fecha`, `estado`, `codigo_postal_administracion`, etc.).
    -   Se ajustaron restricciones `NOT NULL` y `CHECK`.
-   **Índices (`database/indexes.sql`)**: Se crearon índices específicos para optimizar las consultas más frecuentes, incluyendo índices parciales y sobre columnas `LOWER` para búsquedas `ILIKE`.
-   **Vistas (`database/views.sql`)**: Se introdujo una vista materializada (`vm_codigos_postales`) para precalcular los joins y acelerar las consultas complejas.
-   **Funciones (`database/functions.sql`)**: Se implementaron funciones PL/pgSQL para encapsular la lógica de consulta de los endpoints de la API, incluyendo validación de parámetros y paginación.

## 3. Script Python (v2)

El script original (`sepomex_sql_generator.py`) fue completamente refactorizado y movido a `src/`:

-   **Modularización**: La lógica se separó en módulos cohesivos:
    -   `main.py`: Orquestador principal.
    -   `config.py`: Configuraciones centralizadas.
    -   `data_reader.py`: Lectura de datos.
    -   `data_validator.py`: Validación de datos.
    -   `sql_generator.py`: Generación de archivos SQL (incluye batching).
    -   `models.py`: Data Classes para representar entidades.
    -   `utils.py`: Funciones de utilidad (limpieza, formato).
-   **Mejores Prácticas**: 
    -   Se añadieron **Type Hints** y **Docstrings**.
    -   Se implementó **Logging** robusto (reemplazando `print`), enviando salida a consola y archivo (`logs/`).
    -   Se mejoró el **manejo de errores** con excepciones.
    -   Se sigue el estándar PEP 8 (formato con `black`).

## 4. Documentación

-   Toda la documentación relevante (especificaciones v2, prompts, resumen de script) se movió a `docs/`.
-   El archivo `README.md` fue actualizado extensamente para reflejar la nueva estructura, el proceso de instalación/configuración v2, y las características optimizadas.

## 5. Código Heredado (v1)

-   Todos los archivos pertenecientes a la versión inicial/v1 (script original, schema, datos generados, queries) fueron movidos al directorio `legacy_v1/` para mantener el repositorio limpio pero conservar el historial.

## 6. Consultas (v2)

-   Se crearon nuevos archivos SQL en `queries/` (`detailed_lookup_v2.sql`, `testing_v2.sql`) con ejemplos y pruebas adaptados específicamente a la estructura y funciones de la v2.    

Notas:

-   Se actualizó `README.md` para reflejar la nueva estructura de directorios.
-   Se actualizó `database_v2` a `database` una vez movido el código legacy a `legacy_v1/`.
-   Se agrego licencia MIT `LICENSE` ya que en la versión 1 no estaba presente.

