import logging
import sys
import time

from .config import LOG_FILE, LOG_LEVEL, LOG_FORMAT
from .data_reader import read_sepomex_data
from .data_validator import validate_dataframe
from .sql_generator import (
    generate_estados_sql,
    generate_municipios_sql,
    generate_tipos_asentamiento_sql,
    generate_zonas_sql,
    generate_ciudades_sql,
    generate_codigos_postales_sql,
)

def setup_logging():
    """Configura el sistema de logging para archivo y consola."""
    log_level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Punto de entrada principal para la generación de archivos SQL."""
    setup_logging()
    logger = logging.getLogger(__name__)
    start_time = time.time()

    logger.info("--- Iniciando proceso de generación de SQL para SEPOMEX v2 ---")

    # 1. Leer datos
    df_raw = read_sepomex_data()
    if df_raw is None:
        logger.error("No se pudieron leer los datos. Terminando proceso.")
        return

    # 2. Validar datos (Opcional, podría ralentizar si se valida todo)
    # Si se omite, la validación se hace registro a registro en sql_generator
    # df_validated = validate_dataframe(df_raw)
    # if df_validated.empty:
    #     logger.warning("No hay datos válidos después de la validación. No se generarán archivos SQL.")
    #     return
    # df_to_process = df_validated

    # Usar datos crudos y validar dentro de cada generador
    df_to_process = df_raw

    # 3. Generar archivos SQL (en orden de dependencias)
    logger.info("--- Iniciando generación de archivos SQL ---")
    counts = {}
    counts["estados"] = generate_estados_sql(df_to_process)
    counts["municipios"] = generate_municipios_sql(df_to_process)
    counts["tipos_asentamiento"] = generate_tipos_asentamiento_sql(df_to_process)
    counts["zonas"] = generate_zonas_sql() # Zonas no depende del df
    counts["ciudades"] = generate_ciudades_sql(df_to_process)

    # Generar códigos postales (devuelve insertados y errores)
    cp_inserted, cp_errors = generate_codigos_postales_sql(df_to_process)
    counts["codigos_postales"] = cp_inserted

    end_time = time.time()
    duration = end_time - start_time

    # 4. Resumen final
    logger.info("--- Proceso completado ---")
    logger.info("Resumen de registros generados:")
    for entity, count in counts.items():
        logger.info(f"  - {entity.capitalize()}: {count}")
    if cp_errors > 0:
        logger.warning(f"Se encontraron {cp_errors} errores al procesar códigos postales.")
    logger.info(f"Tiempo total de ejecución: {duration:.2f} segundos.")
    logger.info(f"Archivos SQL generados en: {config.OUTPUT_DIR}")
    logger.info(f"Log detallado disponible en: {LOG_FILE}")

if __name__ == "__main__":
    from src import config
    main() 