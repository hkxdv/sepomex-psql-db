import pandas as pd
import re
from typing import Optional
import logging
import sys # Añadido para tabla de traducción

# Crear tabla de traducción para eliminar caracteres de control C1 (0x80-0x9F)
# Estos a menudo causan problemas entre windows-1252 y utf-8
C1_CONTROLS = ''.join(map(chr, range(0x80, 0xA0)))
C1_TRANSLATOR = str.maketrans('', '', C1_CONTROLS)

from .config import (
    MAX_LEN_NOMBRE,
    MAX_LEN_NOMBRE_ASENTAMIENTO,
    DEFAULT_ZONA_NAME,
)

logger = logging.getLogger(__name__)


def clean_text(text: Optional[str], max_length: int = MAX_LEN_NOMBRE) -> str:
    """
    Limpia texto: escapa comillas SQL, normaliza espacios, trunca a longitud máxima.
    Elimina caracteres no compatibles con UTF-8.
    Conserva caracteres especiales como acentos y eñes.

    Args:
        text (Optional[str]): Texto a limpiar.
        max_length (int): Longitud máxima permitida.

    Returns:
        str: Texto limpio, escapado y truncado.
    """
    if pd.isna(text) or text is None:
        return ""

    result = str(text)

    # 1. Eliminar caracteres de control C1 problemáticos
    result = result.translate(C1_TRANSLATOR)

    # 2. Forzar codificación/decodificación UTF-8 como fallback (opcional, pero seguro)
    original_for_debug = result # Guardar antes de encode/decode para comparar
    try:
        result = result.encode('utf-8', errors='ignore').decode('utf-8')
    except Exception:
        # Si falla incluso ignorando, intentar con reemplazo
        try:
            result = result.encode('utf-8', errors='replace').decode('utf-8')
        except Exception:
            # Caso extremo: devolver cadena vacía si la limpieza falla completamente
            logger.warning(f"No se pudo limpiar/codificar el texto: {text[:50]}...")
            return ""

    # Log si el texto cambió durante la codificación/decodificación (útil para debug)
    if logger.isEnabledFor(logging.DEBUG) and original_for_debug != result:
        logger.debug(f"Texto cambiado por encode/decode UTF-8: Original='{original_for_debug[:50]}...', Limpio='{result[:50]}...'")

    replacements = {
        "'": "''",
        '"': '""',
        "\\": "/",
    }

    result = " ".join(result.split()).strip()[:max_length]

    for old, new in replacements.items():
        result = result.replace(old, new)

    # Volver a truncar por si los reemplazos alargaron el string
    final_result = result[:max_length]

    # Log final de la limpieza si está en DEBUG
    if logger.isEnabledFor(logging.DEBUG) and text != final_result:
         logger.debug(f"clean_text: IN='{str(text)[:50]}...' -> OUT='{final_result[:50]}...'")

    return final_result


def format_codigo(codigo: Optional[str | int | float], digits: int = 2) -> Optional[str]:
    """
    Formatea códigos numéricos a una longitud fija con ceros a la izquierda.

    Maneja NaN, None, strings vacíos, números flotantes (truncando decimales)
    y valida que el número no sea negativo.

    Args:
        codigo (Optional[str | int | float]): Código a formatear.
        digits (int): Número de dígitos esperados.

    Returns:
        Optional[str]: Código formateado o None si es inválido/no formateable.
    """
    if pd.isna(codigo) or codigo is None:
        return None

    codigo_str = str(codigo).strip()
    if not codigo_str or codigo_str.lower() == "nan":
        return None

    try:
        if "." in codigo_str:
            codigo_int = int(float(codigo_str))
        else:
            codigo_int = int(codigo_str)

        if codigo_int < 0:
            return None

        return str(codigo_int).zfill(digits)
    except (ValueError, TypeError):
        return None


def normalize_zona(zona_texto: Optional[str]) -> str:
    """
    Normaliza los tipos de zona a 'Urbano', 'Rural' o 'Semiurbano'.

    Args:
        zona_texto (Optional[str]): Texto original de la zona.

    Returns:
        str: Nombre de zona normalizado ('Urbano', 'Rural' o 'Semiurbano').
             Devuelve DEFAULT_ZONA_NAME si la entrada es nula o no coincide.
    """
    if pd.isna(zona_texto) or zona_texto is None:
        return DEFAULT_ZONA_NAME

    zona_limpia = " ".join(str(zona_texto).split()).strip().title()

    if zona_limpia == "Urbano":
        return "Urbano"
    elif zona_limpia == "Rural":
        return "Rural"
    else:
        return DEFAULT_ZONA_NAME 