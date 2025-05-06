# SEPOMEX PostgreSQL Database v2

Base de datos PostgreSQL **optimizada** con códigos postales de México, basada en datos del Servicio Postal Mexicano (SEPOMEX).

<div align="center">
  <img src="https://img.shields.io/badge/-PostgreSQL-000000?style=for-the-badge&logo=postgresql&labelColor=282c34" style="border-radius: 3px;" />
  <img src="https://img.shields.io/badge/-Python-000000?style=for-the-badge&logo=python&labelColor=282c34" style="border-radius: 3px;" />
</div>

## Descripción General

Este proyecto proporciona:

1.  Un **esquema de base de datos PostgreSQL v2** normalizado (3FN) y optimizado para consultas rápidas, utilizando convenciones de nomenclatura claras (`pk_`, `fk_`).
2.  Un **script Python refactorizado** (`src/main.py`) que procesa los datos originales de SEPOMEX y genera archivos SQL para poblar la base de datos v2.
3.  La **fuente de datos original** de SEPOMEX (actualizada a 2021-10-01).
4.  **Documentación detallada** sobre las optimizaciones y el diseño de la v2.

> [!CAUTION]
>
> Este repositorio es una implementación de referencia con fines educativos y de aprendizaje. **No es una fuente oficial de datos de SEPOMEX.**

## Fuente de Datos

Los datos originales provienen del Servicio Postal Mexicano (SEPOMEX) a través de su página oficial, aunque fueron obtenidos de [VIDELCLOUD](https://videlcloud.wordpress.com/2017/01/17/descarga-la-base-de-datos-de-codigos-postales-colonias-municipios-y-estados-de-todo-mexico/) que mantiene una copia actualizada al 2021-10-01.

> [!WARNING]
>
> **Limitaciones y Advertencias**
>
> - Los datos **no son oficiales** y provienen de una copia de 2021.
> - Para información actualizada y oficial, consulte directamente con **SEPOMEX**.
> - Se conservan acentos y caracteres especiales en los nombres.

## Estructura del Proyecto

```plaintext
sepomex-psql-db/
├── data/
│   ├── input/
│   │   └── sepomex_data.txt   # Archivo de datos original
│   └── generated_sql_v2/      # Archivos SQL generados por el script v2
│       ├── ... (001 a 006)
├── database/               # Definición de la BD v2 (Schema, Funciones, Índices, Vistas)
│   ├── schema.sql
│   ├── functions.sql
│   ├── indexes.sql
│   └── views.sql
├── src/                       # Código fuente del generador SQL v2
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── data_reader.py
│   ├── data_validator.py
│   ├── sql_generator.py
│   ├── models.py
│   └── utils.py
├── docs/
│   ├── SEPOMEX_V2.md          # Especificaciones detalladas v2
│   └── ...
├── legacy_v1/                 # Código y artefactos de la v1 (obsoleta)
│   └── ...
├── requirements.txt           # Dependencias Python
├── .gitignore                 # Ignorar archivos generados
├── pyproject.toml             # Configuración (black, isort)
└── README.md
```

## Configuración y Poblado de la Base de Datos

> [!NOTE]
>
> **Distribución Futura con Docker:** Se planea distribuir esta base de datos como una imagen Docker preconfigurada y poblada para facilitar su uso. Consulte futuras actualizaciones de este repositorio.

**Configuración Manual (si la imagen Docker no está disponible):**

Si la imagen Docker aún no está disponible o prefiere una configuración manual, siga estos pasos:

1.  **Requisitos Previos:**

    - PostgreSQL
    - Python
    - Git

2.  **Clonar Repositorio:**

    ```bash
    git clone https://github.com/hkxdv/sepomex-psql-db.git
    cd sepomex-psql-db
    ```

3.  **Entorno Python:** Configure un entorno virtual e instale dependencias:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Generar Archivos SQL:** Ejecute el script Python para crear los archivos de inserción:

    ```bash
    python -m src.main
    ```

    (Los archivos `.sql` se generarán en `data/generated_sql_v2/`)

> [!TIP]
>
> El script generará un archivo de log detallado en `logs/sepomex_generator.log`.
> Puedes ver un ejemplo de la salida del log en **[docs/log_example.md](docs/log_example.md)**.

5.  **Crear y Estructurar Base de Datos:** Cree una base de datos PostgreSQL (ej. `sepomex_psql_db_v2`) y aplique la estructura:

- En orden:
  - `schema.sql`
  - `indexes.sql`
  - `views.sql`
  - `functions.sql`

6.  **Importar Datos:** Ejecute los scripts SQL generados en el paso 5, **en orden numérico**, dentro del directorio `data/generated_sql_v2/`:

## Consultas de Ejemplo

Para ver ejemplos de consultas detalladas usando las funciones PL/pgSQL y consultas para verificar la integridad, consulta:

- **[queries/detailed_lookup_v2](queries/detailed_lookup_v2.sql)**.
- **[queries/testing_v2](queries/testing_v2.sql)**.

## Estructura de la Base de Datos

Para una descripción detallada de las optimizaciones, el análisis de endpoints y las especificaciones completas, consulta: **[docs/SEPOMEX_V2.md](docs/SEPOMEX_V2.md)**.

> [!NOTE]
>
> El documento `SEPOMEX_V2.md` incluye un análisis sobre la "duplicidad funcional" observada en los datos fuente (registros distintos con campos similares).

## Proyecto Relacionado

Se ha desarrollado una API REST complementaria para esta base de datos v2:

<a href="https://github.com/hkxdv/sepomex-api-rest">
  <img src="https://img.shields.io/badge/-sepomex--api--rest-000000?style=for-the-badge&logo=github&labelColor=282c34" style="border-radius: 3px;" />
</a>

La API proporciona endpoints para consultas basadas en las funciones optimizadas de la BD v2.

## 🥷 Autor

<a href="https://github.com/hkxdv">
  <img src="https://img.shields.io/badge/-hkxdv-000000?style=for-the-badge&logo=github&labelColor=282c34" style="border-radius: 3px;" />
</a>
