import pandas as pd
import re
import logging
from typing import Any

from .config import (
    MAX_LEN_NOMBRE,
    MAX_LEN_NOMBRE_ASENTAMIENTO,
    REGEX_CODIGO_POSTAL,
    REGEX_CODIGO_ESTADO,
    REGEX_CODIGO_MUNICIPIO,
    REGEX_CODIGO_CIUDAD,
    REGEX_CODIGO_TIPO_ASENTA,
)
from .utils import format_codigo, clean_text

logger = logging.getLogger(__name__)

def verify_length(value: Any, max_length: int, field_name: str, row_idx: int) -> bool:
    """
    Verifica que un valor no exceda la longitud máxima esperada.

    Args:
        value (Any): Valor a verificar (se convertirá a string).
        max_length (int): Longitud máxima permitida.
        field_name (str): Nombre del campo (para mensajes de log).
        row_idx (int): Índice de la fila (para mensajes de log).

    Returns:
        bool: True si es válido o nulo, False si excede la longitud.
    """
    if value is None or pd.isna(value):
        return True

    value_str = str(value)
    if len(value_str) > max_length:
        logger.warning(
            f"Fila {row_idx}: Longitud inválida en '{field_name}'. "
            f"Valor: '{value_str[:20]}...' (longitud {len(value_str)}), "
            f"máximo permitido: {max_length}."
        )
        return False
    return True

def validate_regex(value: Any, pattern: str, field_name: str, row_idx: int) -> bool:
    """
    Verifica que un valor cumpla con un patrón regex.

    Args:
        value (Any): Valor a verificar (se convertirá a string).
        pattern (str): Patrón regex a aplicar.
        field_name (str): Nombre del campo (para mensajes de log).
        row_idx (int): Índice de la fila (para mensajes de log).

    Returns:
        bool: True si cumple el patrón o es nulo/vacío, False si no cumple.
    """
    if value is None or pd.isna(value) or str(value).strip() == "":
        return True

    value_str = str(value).strip()
    if not re.match(pattern, value_str):
        logger.warning(
            f"Fila {row_idx}: Formato inválido en '{field_name}'. "
            f"Valor: '{value_str}', Patrón esperado: {pattern}."
        )
        return False
    return True

def validate_not_empty(value: Any, field_name: str, row_idx: int) -> bool:
    """
    Verifica que un valor no sea nulo, NaN o un string vacío.

    Args:
        value (Any): Valor a verificar.
        field_name (str): Nombre del campo (para mensajes de log).
        row_idx (int): Índice de la fila (para mensajes de log).

    Returns:
        bool: True si el valor no está vacío, False si lo está.
    """
    is_empty = pd.isna(value) or (isinstance(value, str) and not value.strip())
    if is_empty:
        logger.warning(f"Fila {row_idx}: Campo requerido '{field_name}' está vacío o nulo.")
        return False
    return True

def validate_row(row: pd.Series, row_idx: int) -> bool:
    """
    Valida una fila completa del DataFrame según las reglas v2.

    Aplica validaciones de nulabilidad, longitud y formato regex.

    Args:
        row (pd.Series): Fila del DataFrame a validar.
        row_idx (int): Índice original de la fila (para logging).

    Returns:
        bool: True si la fila es válida, False si tiene algún error.
    """
    is_valid = True

    # Validaciones de nulabilidad para campos requeridos en codigos_postales v2
    is_valid &= validate_not_empty(row.get('d_codigo'), 'd_codigo', row_idx)
    is_valid &= validate_not_empty(row.get('d_asenta'), 'd_asenta', row_idx)
    is_valid &= validate_not_empty(row.get('c_estado'), 'c_estado', row_idx)
    is_valid &= validate_not_empty(row.get('c_tipo_asenta'), 'c_tipo_asenta', row_idx)
    
    # Nombres requeridos para las tablas de catálogo
    is_valid &= validate_not_empty(row.get('d_estado'), 'd_estado', row_idx)
    is_valid &= validate_not_empty(row.get('d_tipo_asenta'), 'd_tipo_asenta', row_idx)
    
    # Municipio y Ciudad pueden ser null, pero si existen, d_mnpio/d_ciudad deben existir
    if pd.notna(row.get('c_mnpio')):
        is_valid &= validate_not_empty(row.get('D_mnpio'), 'D_mnpio', row_idx)
    if pd.notna(row.get('c_cve_ciudad')):
         is_valid &= validate_not_empty(row.get('d_ciudad'), 'd_ciudad', row_idx)

    # Validaciones de formato (Regex)
    is_valid &= validate_regex(row.get('d_codigo'), REGEX_CODIGO_POSTAL, 'd_codigo', row_idx)
    is_valid &= validate_regex(row.get('c_estado'), REGEX_CODIGO_ESTADO, 'c_estado', row_idx)
    is_valid &= validate_regex(row.get('c_mnpio'), REGEX_CODIGO_MUNICIPIO, 'c_mnpio', row_idx)
    is_valid &= validate_regex(row.get('c_cve_ciudad'), REGEX_CODIGO_CIUDAD, 'c_cve_ciudad', row_idx)
    is_valid &= validate_regex(row.get('c_tipo_asenta'), REGEX_CODIGO_TIPO_ASENTA, 'c_tipo_asenta', row_idx)

    # Validaciones de longitud
    is_valid &= verify_length(clean_text(row.get('d_asenta'), MAX_LEN_NOMBRE_ASENTAMIENTO), MAX_LEN_NOMBRE_ASENTAMIENTO, 'd_asenta', row_idx)
    is_valid &= verify_length(clean_text(row.get('d_estado'), MAX_LEN_NOMBRE), MAX_LEN_NOMBRE, 'd_estado', row_idx)
    is_valid &= verify_length(clean_text(row.get('D_mnpio'), MAX_LEN_NOMBRE), MAX_LEN_NOMBRE, 'D_mnpio', row_idx)
    is_valid &= verify_length(clean_text(row.get('d_ciudad'), MAX_LEN_NOMBRE), MAX_LEN_NOMBRE, 'd_ciudad', row_idx)
    is_valid &= verify_length(clean_text(row.get('d_tipo_asenta'), MAX_LEN_NOMBRE), MAX_LEN_NOMBRE, 'd_tipo_asenta', row_idx)

    return is_valid

def validate_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida un DataFrame completo fila por fila.

    Registra errores usando logging y devuelve un DataFrame
    conteniendo solo las filas válidas.

    Args:
        df (pd.DataFrame): DataFrame a validar.

    Returns:
        pd.DataFrame: DataFrame filtrado con solo filas válidas.
    """
    logger.info(f"Iniciando validación de {len(df)} registros...")
    valid_indices = []
    invalid_count = 0

    for idx, row in df.iterrows():
        if validate_row(row, idx + 2):
            valid_indices.append(idx)
        else:
            invalid_count += 1

    valid_percentage = (len(valid_indices) / len(df)) * 100 if len(df) > 0 else 0
    logger.info(
        f"Validación completada. Registros válidos: {len(valid_indices)} ({valid_percentage:.2f}%). "
        f"Registros inválidos: {invalid_count}."
    )
    if invalid_count > 0:
        logger.warning(f"Se encontraron {invalid_count} filas con errores. Revise el log para detalles.")

    return df.loc[valid_indices].copy()