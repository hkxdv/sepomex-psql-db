# SEPOMEX PostgreSQL Database

Base de datos PostgreSQL optimizada con códigos postales de México, basada en datos del Servicio Postal Mexicano (SEPOMEX).

<div align="center">
  <img src="https://img.shields.io/badge/-PostgreSQL-000000?style=for-the-badge&logo=postgresql&labelColor=282c34" style="border-radius: 3px;" />
  <img src="https://img.shields.io/badge/-Python-000000?style=for-the-badge&logo=python&labelColor=282c34" style="border-radius: 3px;" />
</div>

## Fuente de Datos

Los datos originales provienen del Servicio Postal Mexicano (SEPOMEX) a través de su página oficial, aunque fueron obtenidos de [VIDELCLOUD](https://videlcloud.wordpress.com/2017/01/17/descarga-la-base-de-datos-de-codigos-postales-colonias-municipios-y-estados-de-todo-mexico/) que mantiene una copia actualizada al 2021-10-01.

> [!NOTE]
>
> - Última actualización: 2021-10-01
> - Incluye códigos postales, colonias y municipios de todo México
> - Los asentamientos pueden ser: colonias, fraccionamientos, barrios, ejidos, etc.
> - Se conservan acentos y caracteres especiales en los nombres

## Estructura del Proyecto

```
sepomex-psql-db/
├── backup/
│   └── sepomex_backup.sql               # Backup en formato SQL
│
├── data/
│   ├── 001_insert_estados.sql           # Inserción de estados
│   ├── 002_insert_municipios.sql        # Inserción de municipios
│   ├── 003_insert_tipos_asentamiento.sql# Inserción de tipos de asentamiento
│   ├── 004_insert_zonas.sql             # Inserción de zonas
│   ├── 005_insert_ciudades.sql          # Inserción de ciudades
│   └── 006_insert_codigos_postales.sql  # Inserción de códigos postales
│
├── query/
│   ├── queries_detailed_lookup.sql      # Consultas detalladas
│   └── queries_testing.sql              # Consultas de prueba y verificación
│
├── sepomex_sql_generator.py             # Script de procesamiento de datos
├── sepomex_original_data.txt            # Archivo de datos original
└── sepomex_schema.sql                   # Estructura de las tablas de base de datos
```

## Instalación

### Requisitos previos

- PostgreSQL 16.0 o superior
- Python 3.12 o superior
- pandas (`pip install pandas`)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/hk4u-dxv/sepomex-psql-db.git
cd sepomex-psql-db
```

### Paso 2: Crear la base de datos

```bash
createdb -U postgres sepomex_db
```

### Paso 3: Crear la estructura

```bash
psql -h localhost -U postgres -d sepomex_db -f sepomex_schema.sql
```

### Paso 4: Generar archivos SQL (opcional)

Si necesitas regenerar los archivos SQL:

```bash
python sepomex_sql_generator.py
```

### Paso 5: Importar datos

```bash
cd data
psql -h localhost -U postgres -d sepomex_db -f 001_insert_estados.sql
psql -h localhost -U postgres -d sepomex_db -f 002_insert_municipios.sql
psql -h localhost -U postgres -d sepomex_db -f 003_insert_tipos_asentamiento.sql
psql -h localhost -U postgres -d sepomex_db -f 004_insert_zonas.sql
psql -h localhost -U postgres -d sepomex_db -f 005_insert_ciudades.sql
psql -h localhost -U postgres -d sepomex_db -f 006_insert_codigos_postales.sql
```

> [!IMPORTANT]
> Es crucial seguir este orden de ejecución para mantener la integridad de las relaciones entre tablas.

## Uso y consultas

Ejemplos de consultas básicas:

```sql
-- Buscar por código postal
SELECT * FROM codigos_postales WHERE codigo_postal = '29000';

-- Buscar asentamientos que contengan "centro" en su nombre
SELECT * FROM codigos_postales WHERE nombre_asentamiento ILIKE '%centro%';

-- Buscar por estado y municipio
SELECT cp.* FROM codigos_postales cp
JOIN estados e ON cp.codigo_estado = e.codigo_estado
JOIN municipios m ON cp.codigo_municipio = m.codigo_municipio AND cp.codigo_estado = m.codigo_estado
WHERE e.nombre_estado = 'Chiapas' AND m.nombre_municipio = 'Tuxtla Gutiérrez';
```

Consulta el directorio `query/` para ver más ejemplos de consultas.

## Estructura de la Base de Datos

La base de datos cuenta con las siguientes tablas principales:

1. **estados**: Catálogo de estados de México
2. **municipios**: Catálogo de municipios con relación a estados
3. **ciudades**: Ciudades importantes con relación a estados
4. **tipos_asentamiento**: Catálogo de tipos de asentamiento (colonia, barrio, etc.)
5. **zonas**: Clasificación de zonas (Urbana, Rural, Semiurbana)
6. **codigos_postales**: Tabla principal con todos los códigos postales y sus relaciones

Todas las tablas incluyen timestamps de creación/actualización y restricciones de integridad.

> [!WARNING]
>
> - Los datos son una versión no oficial basada en la estructura de SEPOMEX
> - Última actualización de la fuente de datos: 2021-10-01
> - Para uso oficial, se recomienda consultar directamente con SEPOMEX
> - Este proyecto es una implementación de referencia y educativa

## Proyecto Relacionado

Se ha desarrollado una API REST complementaria para esta base de datos:

<a href="https://github.com/hk4u-dxv/sepomex-api-rest">
  <img src="https://img.shields.io/badge/-sepomex--api--rest-000000?style=for-the-badge&logo=github&labelColor=282c34" style="border-radius: 3px;" />
</a>

La API proporciona endpoints para:

- Consulta de códigos postales
- Búsqueda de asentamientos
- Filtrado por estado/municipio
- Validación de códigos postales

## 🥷 Autor

<a href="https://github.com/hk4u-dxv">
  <img src="https://img.shields.io/badge/-hk4u--dxv-000000?style=for-the-badge&logo=github&labelColor=282c34" style="border-radius: 3px;" />
</a>
