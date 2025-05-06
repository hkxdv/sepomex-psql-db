import pandas as pd
import logging
from typing import Optional

from .config import (
    INPUT_FILE_PATH,
    FILE_ENCODING,
    FILE_SEPARATOR,
    INPUT_COLUMNS_V2,
)

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


def read_sepomex_data() -> Optional[pd.DataFrame]:
    """
    Lee el archivo de datos original de SEPOMEX.

    Utiliza la configuración definida en config.py para la ruta, codificación,
    separador y columnas a leer.

    Returns:
        Optional[pd.DataFrame]: DataFrame con los datos leídos o None si ocurre un error.
    """
    try:
        logger.info(f"Iniciando lectura del archivo: {INPUT_FILE_PATH}")

        # Definir tipos de datos para columnas de códigos para asegurar que se lean como strings
        dtype_map = {
            col: str for col in INPUT_COLUMNS_V2
            if col.startswith('c_') or col == 'd_codigo'
        }

        df = pd.read_csv(
            INPUT_FILE_PATH,
            sep=FILE_SEPARATOR,
            encoding=FILE_ENCODING,
            usecols=lambda c: c in INPUT_COLUMNS_V2,
            dtype=dtype_map,
            low_memory=False,
        )

        logger.info(f"Lectura completada. {len(df)} registros leídos.")
        logger.debug(f"Columnas cargadas: {df.columns.tolist()}")

        # Verificar si faltan columnas esenciales (excepto d_zona que es opcional)
        columnas_cargadas = df.columns.tolist()
        columnas_faltantes = [
            col for col in INPUT_COLUMNS_V2
            if col not in columnas_cargadas and col != 'd_zona'
        ]
        if columnas_faltantes:
            logger.warning("Faltan columnas esenciales en el archivo fuente:")
            for col in columnas_faltantes:
                logger.warning(f"  - {col}")

        return df

    except FileNotFoundError:
        logger.exception(f"Error crítico: Archivo no encontrado en {INPUT_FILE_PATH}")
        return None
    except ValueError as ve:
        logger.exception("Error de valor durante la lectura (¿columnas faltantes?)")
        logger.error(f"Detalle: {ve}")
        logger.error(f"Columnas esperadas: {INPUT_COLUMNS_V2}")
        return None
    except Exception as e:
        logger.exception("Error inesperado durante la lectura del archivo.")
        return None 