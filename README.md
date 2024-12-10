# Base de Datos SEPOMEX

Base de datos PostgreSQL para códigos postales de México basada en datos del Servicio Postal Mexicano (SEPOMEX).

<div align="center">

![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-000000?style=for-the-badge&logo=postgresql&labelColor=282c34)
![Python](https://img.shields.io/badge/-Python-000000?style=for-the-badge&logo=python&labelColor=282c34)

</div>

## Fuente de Datos

Los datos originales provienen del servicio postal mexicano (SEPOMEX) a través de su página oficial, aunque fueron obtenidos de [VIDELCLOUD](https://videlcloud.wordpress.com/2017/01/17/descarga-la-base-de-datos-de-codigos-postales-colonias-municipios-y-estados-de-todo-mexico/) que mantiene una copia actualizada al 2021-10-01.

> [!NOTE]
>
> - Última actualización: 2021-10-01
> - Incluye códigos postales, colonias y municipios de todo México
> - Pueden existir algunos errores tipográficos menores
> - El tipo de asentamiento puede ser: colonia, fraccionamiento, barrio, ejido, poblado, unidad habitacional, etc.

## Desarrollo y Conversión

Este proyecto toma el archivo de texto plano (.txt) original y:

1. Diseña una estructura normalizada de base de datos PostgreSQL
2. Implementa un script Python para procesar y convertir los datos
3. Crea índices optimizados para consultas eficientes
4. Establece relaciones y restricciones entre tablas
5. Genera scripts SQL para la inserción ordenada de datos

Todo el trabajo de conversión, estructuración y optimización fue realizado desde cero, partiendo únicamente del archivo de datos original.

## Estructura del Proyecto

```text
sepomex/
├── backup/
│ ├── sepomex_backup.dump                  # Backup en formato binario
│ └── sepomex_backup.sql                   # Backup en formato SQL
│
├── database/
│ ├── 001_insert_estados.sql               # Inserción de estados
│ ├── 002_insert_municipios.sql            # Inserción de municipios
│ ├── 003_insert_tipos_asentamiento.sql    # Inserción de tipos de asentamiento
│ ├── 004_insert_ciudades.sql              # Inserción de ciudades
│ ├── 005_insert_zonas.sql                 # Inserción de zonas
│ └── 006_insert_codigos_postales.sql      # Inserción de códigos postales
│
├── query/
│ ├── consultas_detalle.sql               # Consultas detalladas
│ └── consultas_prueba.sql                # Consultas de prueba y verificación
│
├── generar_sql_cp.py                     # Script de procesamiento de datos
├── sepomex_original_data.txt             # Archivo de datos original
└── sepomex_schema.sql                    # Estructura de las tablas de base de datos
```

## Orden de Ejecución

> [!IMPORTANT]
> Es crucial seguir este orden de ejecución para mantener la integridad de las relaciones entre tablas.

1. Crear la estructura:

   ```bash
   psql -h localhost -U postgres -d sepomex_db -f sepomex_schema.sql
   ```

2. Generar archivos SQL:

   ```bash
   python generar_sql_cp.py
   ```

3. Insertar datos en orden:
   ```bash
   psql -h localhost -U postgres -d sepomex_db -f database/001_insert_estados.sql
   psql -h localhost -U postgres -d sepomex_db -f database/002_insert_municipios.sql
   psql -h localhost -U postgres -d sepomex_db -f database/003_insert_tipos_asentamiento.sql
   psql -h localhost -U postgres -d sepomex_db -f database/004_insert_ciudades.sql
   psql -h localhost -U postgres -d sepomex_db -f database/005_insert_zonas.sql
   psql -h localhost -U postgres -d sepomex_db -f database/006_insert_codigos_postales.sql
   ```

## Notas Importantes y Limitaciones

> [!WARNING]
>
> - Los datos son una versión no oficial basada en la estructura de SEPOMEX
> - Última actualización de la fuente de datos: 2021-10-01
> - Los datos pueden contener errores tipográficos
> - No se garantiza la actualización en tiempo real
> - Para uso oficial, se recomienda consultar directamente con SEPOMEX
> - Este proyecto es una implementación de referencia y educativa

### API REST y Proyecto Relacionado

Se ha desarrollado una API REST complementaria para esta base de datos en el repositorio [sepomex-api-rest](https://github.com/hk4u-dxv/sepomex-api-rest) utilizando:

- Node.js
- Express
- pg (node-postgres)

La API proporciona endpoints para:

- Consulta de códigos postales
- Búsqueda de asentamientos
- Filtrado por estado/municipio
- Validación de códigos postales

- [sepomex-api-rest](https://github.com/hk4u-dxv/sepomex-api-rest) - API REST en Node.js

### 🥷 Autor

<a href="https://github.com/hk4u-dxv">
  <img src="https://img.shields.io/badge/-hk4u--dxv-181717?style=for-the-badge&logo=github&labelColor=282c34" style="border-radius: 3px;" />
</a>
