```bash
PS C:\GitHub\sepomex-psql-db> python -m src.main
2025-05-05 15:29:41,663 - __main__ - INFO - --- Iniciando proceso de generación de SQL para SEPOMEX v2 ---
2025-05-05 15:29:41,664 - src.data_reader - INFO - Iniciando lectura del archivo: C:\GitHub\sepomex-psql-db\data\input\sepomex_data.txt
2025-05-05 15:29:43,432 - src.data_reader - INFO - Lectura completada. 145024 registros leídos.
2025-05-05 15:29:43,433 - __main__ - INFO - --- Iniciando generación de archivos SQL ---
2025-05-05 15:34:03,553 - __main__ - INFO - --- Iniciando proceso de generación de SQL para SEPOMEX v2 ---
2025-05-05 15:34:03,554 - src.data_reader - INFO - Iniciando lectura del archivo: C:\GitHub\sepomex-psql-db\data\input\sepomex_data.txt
2025-05-05 15:34:05,053 - src.data_reader - INFO - Lectura completada. 145024 registros leídos.
2025-05-05 15:34:05,069 - __main__ - INFO - --- Iniciando generación de archivos SQL ---
2025-05-05 15:34:27,367 - src.sql_generator - INFO - Generado SQL para 32 estados en 001_insert_estados.sql
2025-05-05 15:34:51,387 - src.sql_generator - INFO - Generado SQL para 2458 municipios en 002_insert_municipios.sql
2025-05-05 15:35:16,475 - src.sql_generator - INFO - Generado SQL para 34 tipos de asentamiento en 003_insert_tipos_asentamiento.sql
2025-05-05 15:35:16,505 - src.sql_generator - INFO - Generado SQL para 3 zonas en 004_insert_zonas.sql
2025-05-05 15:35:29,392 - src.sql_generator - INFO - Generado SQL para 664 ciudades en 005_insert_ciudades.sql
2025-05-05 15:35:29,398 - src.sql_generator - INFO - Procesando 145024 códigos postales en 15 lotes de tamaño 10000...
2025-05-05 15:36:11,602 - src.sql_generator - INFO - Generado SQL para 145024 códigos postales.
2025-05-05 15:36:11,605 - __main__ - INFO - --- Proceso completado ---
2025-05-05 15:36:11,606 - __main__ - INFO - Resumen de registros generados:
2025-05-05 15:36:11,607 - __main__ - INFO -   - Estados: 32
2025-05-05 15:36:11,608 - __main__ - INFO -   - Municipios: 2458
2025-05-05 15:36:11,612 - __main__ - INFO -   - Tipos_asentamiento: 34
2025-05-05 15:36:11,613 - __main__ - INFO -   - Zonas: 3
2025-05-05 15:36:11,631 - __main__ - INFO -   - Ciudades: 664
2025-05-05 15:36:11,643 - __main__ - INFO -   - Codigos_postales: 145024
2025-05-05 15:36:11,648 - __main__ - INFO - Tiempo total de ejecución: 128.05 segundos.
2025-05-05 15:36:11,682 - __main__ - INFO - Archivos SQL generados en: C:\GitHub\sepomex-psql-db\data\generated_sql_v2
2025-05-05 15:36:11,691 - __main__ - INFO - Log detallado disponible en: C:\GitHub\sepomex-psql-db\logs\sepomex_generator.log
```
