Instalación y ejecución:

```bash
PS ...\sepomex-psql-db> python -m venv .venv
PS ...\sepomex-psql-db> .venv\Scripts\activate
(.venv) PS ...\sepomex-psql-db> python -m pip install -r requirements.txt
(.venv) PS ...\sepomex-psql-db> python -m src.main
```

Salida del log:

```bash
2025-05-05 17:15:41,507 - __main__ - INFO - --- Iniciando proceso de generación de SQL para SEPOMEX v2 ---
2025-05-05 17:15:41,508 - src.data_reader - INFO - Iniciando lectura del archivo: ...\data\input\sepomex_data.txt
2025-05-05 17:15:42,286 - src.data_reader - INFO - Lectura completada. 145024 registros leídos.
2025-05-05 17:15:42,287 - __main__ - INFO - --- Iniciando generación de archivos SQL ---
2025-05-05 17:16:00,303 - src.sql_generator - INFO - Generado SQL para 32 estados en 001_insert_estados.sql
2025-05-05 17:16:19,900 - src.sql_generator - INFO - Generado SQL para 2458 municipios en 002_insert_municipios.sql
2025-05-05 17:16:37,675 - src.sql_generator - INFO - Generado SQL para 34 tipos de asentamiento en 003_insert_tipos_asentamiento.sql
2025-05-05 17:16:37,702 - src.sql_generator - INFO - Generado SQL para 3 zonas en 004_insert_zonas.sql
2025-05-05 17:16:42,879 - src.sql_generator - INFO - Generado SQL para 664 ciudades en 005_insert_ciudades.sql
2025-05-05 17:16:42,886 - src.sql_generator - INFO - Procesando 145024 códigos postales en 15 lotes de tamaño 10000...
2025-05-05 17:16:50,389 - src.utils - DEBUG - clean_text: IN='Chalet "La Cumbre"...' -> OUT='Chalet ""La Cumbre""...'
2025-05-05 17:16:51,444 - src.utils - DEBUG - clean_text: IN='CNOP Sección  A...' -> OUT='CNOP Sección A...'
2025-05-05 17:16:52,055 - src.sql_generator - DEBUG - Procesando lote 6/15 (índices 50000-59999)...
2025-05-05 17:16:52,414 - src.utils - DEBUG - clean_text: IN='San Miguel la  Higa...' -> OUT='San Miguel la Higa...'
2025-05-05 17:16:53,151 - src.utils - DEBUG - clean_text: IN='La Morena Sección Norte "B"...' -> OUT='La Morena Sección Norte ""B""...'
2025-05-05 17:16:53,152 - src.utils - DEBUG - clean_text: IN='La Morena Sección Norte "C"...' -> OUT='La Morena Sección Norte ""C""...'
2025-05-05 17:16:53,805 - src.sql_generator - DEBUG - Procesando lote 7/15 (índices 60000-69999)...
2025-05-05 17:16:54,410 - src.utils - DEBUG - clean_text: IN='La Merced  (Alameda)...' -> OUT='La Merced (Alameda)...'
2025-05-05 17:16:54,456 - src.utils - DEBUG - clean_text: IN='Jesús García Lovera "El Pilar"...' -> OUT='Jesús García Lovera ""El Pilar""...'
2025-05-05 17:16:54,484 - src.utils - DEBUG - clean_text: IN='San Marcos  Yachihuacaltepec...' -> OUT='San Marcos Yachihuacaltepec...'
2025-05-05 17:16:54,656 - src.utils - DEBUG - clean_text: IN='Manzana  Cuarta...' -> OUT='Manzana Cuarta...'
2025-05-05 17:16:54,885 - src.utils - DEBUG - clean_text: IN='Puerto de la  Arena...' -> OUT='Puerto de la Arena...'
2025-05-05 17:16:55,001 - src.utils - DEBUG - clean_text: IN='La Herradura  ( La Soledad )...' -> OUT='La Herradura ( La Soledad )...'
2025-05-05 17:16:55,077 - src.utils - DEBUG - clean_text: IN='Los Ciruelos  (Rancho el Iris)...' -> OUT='Los Ciruelos (Rancho el Iris)...'
2025-05-05 17:16:55,112 - src.utils - DEBUG - clean_text: IN='San Pedro Ejido Tecomatlán  (Ejido Tecomatlán)...' -> OUT='San Pedro Ejido Tecomatlán (Ejido Tecomatlán)...'
2025-05-05 17:16:55,305 - src.utils - DEBUG - clean_text: IN='Tlalnepantla  Centro...' -> OUT='Tlalnepantla Centro...'
2025-05-05 17:16:55,464 - src.utils - DEBUG - clean_text: IN='INFONAVIT Sur "Niños Héroes"...' -> OUT='INFONAVIT Sur ""Niños Héroes""...'
2025-05-05 17:16:55,677 - src.utils - DEBUG - clean_text: IN='Sección Jardín "Las Plazas" (Unidad Coacalco)...' -> OUT='Sección Jardín ""Las Plazas"" (Unidad Coacalco)...'
2025-05-05 17:16:55,742 - src.sql_generator - DEBUG - Procesando lote 8/15 (índices 70000-79999)...
2025-05-05 17:16:57,074 - src.utils - DEBUG - clean_text: IN='Campamento Obrero "Francisco J. Mujica"...' -> OUT='Campamento Obrero ""Francisco J. Mujica""...'
2025-05-05 17:16:57,866 - src.sql_generator - DEBUG - Procesando lote 9/15 (índices 80000-89999)...
2025-05-05 17:16:58,415 - src.utils - DEBUG - clean_text: IN='Tierra y Libertad  ( La Loma )...' -> OUT='Tierra y Libertad ( La Loma )...'
2025-05-05 17:16:58,539 - src.utils - DEBUG - clean_text: IN='Lagos  de Aztlán...' -> OUT='Lagos de Aztlán...'
2025-05-05 17:16:58,903 - src.utils - DEBUG - clean_text: IN='San Bernabé IX  (F-112)...' -> OUT='San Bernabé IX (F-112)...'
2025-05-05 17:16:59,184 - src.utils - DEBUG - clean_text: IN='Privadas de Anáhuac Sector  Mediterráneo...' -> OUT='Privadas de Anáhuac Sector Mediterráneo...'
2025-05-05 17:17:06,902 - src.sql_generator - DEBUG - Procesando lote 13/15 (índices 120000-129999)...
2025-05-05 17:17:08,356 - src.utils - DEBUG - clean_text: IN='Praderas de  Victoria...' -> OUT='Praderas de Victoria...'
2025-05-05 17:17:08,712 - src.sql_generator - DEBUG - Procesando lote 14/15 (índices 130000-139999)...
2025-05-05 17:17:09,802 - src.utils - DEBUG - clean_text: IN='Congreso de la  Unión...' -> OUT='Congreso de la Unión...'
2025-05-05 17:17:10,436 - src.utils - DEBUG - clean_text: IN='Colonia la  Huerta (El Balneario)...' -> OUT='Colonia la Huerta (El Balneario)...'
2025-05-05 17:17:10,550 - src.sql_generator - DEBUG - Procesando lote 15/15 (índices 140000-149999)...
2025-05-05 17:17:10,595 - src.utils - DEBUG - clean_text: IN='Benito Juárez  (Benemérito de las Américas)...' -> OUT='Benito Juárez (Benemérito de las Américas)...'
2025-05-05 17:17:10,597 - src.utils - DEBUG - clean_text: IN='Fernando López Arias  (El Chorrito)...' -> OUT='Fernando López Arias (El Chorrito)...'
2025-05-05 17:17:11,441 - src.sql_generator - INFO - Generado SQL para 145024 códigos postales.
2025-05-05 17:17:11,444 - __main__ - INFO - --- Proceso completado ---
2025-05-05 17:17:11,444 - __main__ - INFO - Resumen de registros generados:
2025-05-05 17:17:11,445 - __main__ - INFO -   - Estados: 32
2025-05-05 17:17:11,446 - __main__ - INFO -   - Municipios: 2458
2025-05-05 17:17:11,446 - __main__ - INFO -   - Tipos_asentamiento: 34
2025-05-05 17:17:11,449 - __main__ - INFO -   - Zonas: 3
2025-05-05 17:17:11,450 - __main__ - INFO -   - Ciudades: 664
2025-05-05 17:17:11,451 - __main__ - INFO -   - Codigos_postales: 145024
2025-05-05 17:17:11,452 - __main__ - INFO - Tiempo total de ejecución: 89.94 segundos.
2025-05-05 17:17:11,453 - __main__ - INFO - Archivos SQL generados en: ...\data\generated_sql_v2
2025-05-05 17:17:11,454 - __main__ - INFO - Log detallado disponible en: ...\logs\sepomex_generator.log
```
