import pandas as pd
import logging
import math
from pathlib import Path
from typing import List, Tuple, Optional, Iterator

from .config import (
    OUTPUT_DIR,
    ZONAS_MAP,
    DEFAULT_ZONA_ID,
    BATCH_SIZE_CODIGOS_POSTALES,
    MAX_LEN_NOMBRE_ASENTAMIENTO,
    REGEX_CODIGO_POSTAL,
    REGEX_CODIGO_ESTADO,
    REGEX_CODIGO_MUNICIPIO,
    REGEX_CODIGO_CIUDAD,
    REGEX_CODIGO_TIPO_ASENTA,
)
from .utils import format_codigo, clean_text, normalize_zona
from .models import (
    Estado,
    Municipio,
    Ciudad,
    TipoAsentamiento,
    Zona,
    CodigoPostal,
)
from .data_validator import validate_regex

logger = logging.getLogger(__name__)

# --- Funciones auxiliares para escribir SQL ---

def _write_sql_file(
    filepath: Path,
    table_name: str,
    columns: List[str],
    values: List[str],
    entity_name: str,
) -> int:
    """
    Escribe un archivo SQL con formato BEGIN/COMMIT y sentencias INSERT.

    Args:
        filepath (Path): Ruta completa del archivo SQL a generar.
        table_name (str): Nombre de la tabla SQL.
        columns (List[str]): Lista de nombres de columnas.
        values (List[str]): Lista de strings con formato "('val1', 'val2', ...)".
        entity_name (str): Nombre de la entidad (para logging, ej: "estados").

    Returns:
        int: Número de registros escritos en el archivo.
    """
    count = len(values)
    try:
        logger.debug(f"Abriendo {filepath.name} para escritura con encoding=utf-8, errors=ignore")
        with open(filepath, "w", encoding="utf-8", errors="ignore") as f:
            f.write("BEGIN;\n")
            if values:
                cols_sql = ", ".join(columns)
                insert_prefix = f"INSERT INTO {table_name} ({cols_sql}) VALUES\n"
                f.write(insert_prefix)
                f.write(",\n".join(values) + ";\n")
                logger.info(f"Generado SQL para {count} {entity_name} en {filepath.name}")
            else:
                f.write(f"-- No se encontraron {entity_name} válidos\n")
                logger.warning(f"No se encontraron {entity_name} válidos para generar {filepath.name}")
            f.write("COMMIT;\n")
        return count
    except IOError as e:
        logger.exception(f"Error al escribir el archivo SQL {filepath.name}")
        return 0
    except Exception as e:
        logger.exception(f"Error inesperado al generar SQL para {entity_name}")
        return 0

# --- Generadores de SQL para cada tabla ---

def generate_estados_sql(df: pd.DataFrame) -> int:
    """
    Genera el archivo SQL para la tabla 'estados'.

    Args:
        df (pd.DataFrame): DataFrame con los datos fuente.

    Returns:
        int: Número de estados insertados.
    """
    filepath = OUTPUT_DIR / "001_insert_estados.sql"
    if "c_estado" not in df.columns or "d_estado" not in df.columns:
        logger.error("Faltan columnas 'c_estado' o 'd_estado' para generar estados.")
        _write_sql_file(filepath, "estados", [], [], "estados")
        return 0

    estados_data: List[Estado] = []
    processed_codes = set()

    for _, row in df.iterrows():
        codigo = format_codigo(row["c_estado"], 2)
        if codigo and codigo not in processed_codes and validate_regex(codigo, REGEX_CODIGO_ESTADO, 'c_estado', _):
            nombre = clean_text(row["d_estado"])
            if nombre:
                estados_data.append(Estado(pk_codigo_estado=codigo, nombre_estado=nombre))
                processed_codes.add(codigo)
            else:
                 logger.debug(f"Estado con código {codigo} omitido por nombre vacío.")

    values = [
        f"('{e.pk_codigo_estado}', '{e.nombre_estado}')"
        for e in estados_data
    ]
    return _write_sql_file(
        filepath,
        "estados",
        ["pk_codigo_estado", "nombre_estado"],
        values,
        "estados",
    )

def generate_municipios_sql(df: pd.DataFrame) -> int:
    """
    Genera el archivo SQL para la tabla 'municipios'.

    Args:
        df (pd.DataFrame): DataFrame con los datos fuente.

    Returns:
        int: Número de municipios insertados.
    """
    filepath = OUTPUT_DIR / "002_insert_municipios.sql"
    required_cols = ["c_mnpio", "c_estado", "D_mnpio"]
    if not all(col in df.columns for col in required_cols):
        logger.error(f"Faltan columnas {required_cols} para generar municipios.")
        _write_sql_file(filepath, "municipios", [], [], "municipios")
        return 0

    municipios_data: List[Municipio] = []
    processed_pks = set()

    for _, row in df.iterrows():
        codigo_mnpio = format_codigo(row["c_mnpio"], 3)
        codigo_estado = format_codigo(row["c_estado"], 2)
        pk_tuple = (codigo_mnpio, codigo_estado)

        if (
            codigo_mnpio and codigo_estado and pk_tuple not in processed_pks and
            validate_regex(codigo_mnpio, REGEX_CODIGO_MUNICIPIO, 'c_mnpio', _) and
            validate_regex(codigo_estado, REGEX_CODIGO_ESTADO, 'c_estado', _)
        ):
            nombre = clean_text(row["D_mnpio"])
            if nombre:
                municipios_data.append(Municipio(
                    pk_codigo_municipio=codigo_mnpio,
                    fk_codigo_estado=codigo_estado,
                    nombre_municipio=nombre
                ))
                processed_pks.add(pk_tuple)
            else:
                 logger.debug(f"Municipio {pk_tuple} omitido por nombre vacío.")

    values = [
        f"('{m.pk_codigo_municipio}', '{m.fk_codigo_estado}', '{m.nombre_municipio}')"
        for m in municipios_data
    ]
    return _write_sql_file(
        filepath,
        "municipios",
        ["pk_codigo_municipio", "fk_codigo_estado", "nombre_municipio"],
        values,
        "municipios",
    )

def generate_tipos_asentamiento_sql(df: pd.DataFrame) -> int:
    """
    Genera el archivo SQL para la tabla 'tipos_asentamiento'.

    Args:
        df (pd.DataFrame): DataFrame con los datos fuente.

    Returns:
        int: Número de tipos de asentamiento insertados.
    """
    filepath = OUTPUT_DIR / "003_insert_tipos_asentamiento.sql"
    required_cols = ["c_tipo_asenta", "d_tipo_asenta"]
    if not all(col in df.columns for col in required_cols):
        logger.error(f"Faltan columnas {required_cols} para generar tipos de asentamiento.")
        _write_sql_file(filepath, "tipos_asentamiento", [], [], "tipos de asentamiento")
        return 0

    tipos_data: List[TipoAsentamiento] = []
    processed_codes = set()

    df_sorted = df.sort_values(by='d_tipo_asenta', na_position='last')

    for _, row in df_sorted.iterrows():
        codigo = format_codigo(row["c_tipo_asenta"], 2)
        if codigo and codigo not in processed_codes and validate_regex(codigo, REGEX_CODIGO_TIPO_ASENTA, 'c_tipo_asenta', _):
            nombre = clean_text(row["d_tipo_asenta"])
            if nombre:
                tipos_data.append(TipoAsentamiento(
                    pk_codigo_tipo_asentamiento=codigo,
                    nombre_tipo_asentamiento=nombre
                ))
                processed_codes.add(codigo)
            else:
                 logger.debug(f"Tipo asentamiento {codigo} omitido por nombre vacío.")

    values = [
        f"('{t.pk_codigo_tipo_asentamiento}', '{t.nombre_tipo_asentamiento}')"
        for t in tipos_data
    ]
    return _write_sql_file(
        filepath,
        "tipos_asentamiento",
        ["pk_codigo_tipo_asentamiento", "nombre_tipo_asentamiento"],
        values,
        "tipos de asentamiento",
    )

def generate_zonas_sql() -> int:
    """
    Genera el archivo SQL para la tabla 'zonas' con valores fijos.

    Returns:
        int: Número de zonas insertadas (siempre 3 si tiene éxito).
    """
    filepath = OUTPUT_DIR / "004_insert_zonas.sql"
    zonas_data: List[Zona] = []
    try:
        for nombre, pk_id in ZONAS_MAP.items():
            nombre_limpio = clean_text(nombre)
            if nombre_limpio:
                 zonas_data.append(Zona(pk_id_zona=pk_id, nombre_zona=nombre_limpio))
    except Exception as e:
         logger.error(f"Error creando datos de Zonas: {e}")
         zonas_data = []

    values = [
        f"({z.pk_id_zona}, '{z.nombre_zona}')" for z in zonas_data
    ]
    return _write_sql_file(
        filepath,
        "zonas",
        ["pk_id_zona", "nombre_zona"],
        values,
        "zonas",
    )

def generate_ciudades_sql(df: pd.DataFrame) -> int:
    """
    Genera el archivo SQL para la tabla 'ciudades'.

    Args:
        df (pd.DataFrame): DataFrame con los datos fuente.

    Returns:
        int: Número de ciudades insertadas.
    """
    filepath = OUTPUT_DIR / "005_insert_ciudades.sql"
    required_cols = ["c_cve_ciudad", "c_estado", "d_ciudad"]
    if not all(col in df.columns for col in required_cols):
        logger.warning(f"Faltan columnas {required_cols} para generar ciudades. El archivo estará vacío.")
        _write_sql_file(filepath, "ciudades", [], [], "ciudades")
        return 0

    ciudades_data: List[Ciudad] = []
    processed_pks = set()

    df_filtered = df.dropna(subset=required_cols)

    for _, row in df_filtered.iterrows():
        codigo_ciudad = format_codigo(row["c_cve_ciudad"], 2)
        codigo_estado = format_codigo(row["c_estado"], 2)
        pk_tuple = (codigo_ciudad, codigo_estado)

        if (
            codigo_ciudad and codigo_estado and pk_tuple not in processed_pks and
            validate_regex(codigo_ciudad, REGEX_CODIGO_CIUDAD, 'c_cve_ciudad', _) and
            validate_regex(codigo_estado, REGEX_CODIGO_ESTADO, 'c_estado', _)
        ):
            nombre = clean_text(row["d_ciudad"])
            if nombre:
                ciudades_data.append(Ciudad(
                    pk_codigo_ciudad=codigo_ciudad,
                    fk_codigo_estado=codigo_estado,
                    nombre_ciudad=nombre
                ))
                processed_pks.add(pk_tuple)
            else:
                 logger.debug(f"Ciudad {pk_tuple} omitida por nombre vacío.")

    values = [
        f"('{c.pk_codigo_ciudad}', '{c.fk_codigo_estado}', '{c.nombre_ciudad}')"
        for c in ciudades_data
    ]
    return _write_sql_file(
        filepath,
        "ciudades",
        ["pk_codigo_ciudad", "fk_codigo_estado", "nombre_ciudad"],
        values,
        "ciudades",
    )


def _process_cp_batch(df_batch: pd.DataFrame) -> Tuple[List[str], int]:
    """
    Procesa un lote del DataFrame para generar valores SQL de codigos_postales.

    Args:
        df_batch (pd.DataFrame): Lote del DataFrame a procesar.

    Returns:
        Tuple[List[str], int]: Tupla con la lista de valores SQL y el contador de errores.
    """
    valores_batch = []
    errores_batch = 0

    for idx, row in df_batch.iterrows():
        try:
            codigo_postal = format_codigo(row.get("d_codigo"), 5)
            fk_estado = format_codigo(row.get("c_estado"), 2)
            fk_tipo_asenta = format_codigo(row.get("c_tipo_asenta"), 2)
            nombre_asenta = clean_text(row.get('d_asenta'), MAX_LEN_NOMBRE_ASENTAMIENTO)

            zona_norm = normalize_zona(row.get("d_zona"))
            fk_zona = ZONAS_MAP.get(zona_norm, DEFAULT_ZONA_ID)

            valid = True
            if not validate_regex(codigo_postal, REGEX_CODIGO_POSTAL, 'd_codigo', idx):
                 valid = False
            if not nombre_asenta:
                 logger.warning(f"Fila {idx}: Nombre de asentamiento vacío omitido.")
                 valid = False
            if not validate_regex(fk_estado, REGEX_CODIGO_ESTADO, 'c_estado', idx):
                 valid = False
            if not validate_regex(fk_tipo_asenta, REGEX_CODIGO_TIPO_ASENTA, 'c_tipo_asenta', idx):
                 valid = False

            if not valid:
                errores_batch += 1
                continue

            fk_municipio_fmt = format_codigo(row.get("c_mnpio"), 3)
            fk_municipio = f"'{fk_municipio_fmt}'" if fk_municipio_fmt and validate_regex(fk_municipio_fmt, REGEX_CODIGO_MUNICIPIO, 'c_mnpio', idx) else "NULL"

            fk_ciudad_fmt = format_codigo(row.get("c_cve_ciudad"), 2)
            fk_ciudad = f"'{fk_ciudad_fmt}'" if fk_ciudad_fmt and validate_regex(fk_ciudad_fmt, REGEX_CODIGO_CIUDAD, 'c_cve_ciudad', idx) else "NULL"

            valor = f"('{codigo_postal}', '{nombre_asenta}', '{fk_estado}', {fk_municipio}, {fk_ciudad}, '{fk_tipo_asenta}', {fk_zona})"
            valores_batch.append(valor)

        except Exception as e:
            logger.error(f"Error procesando fila {idx} para códigos postales: {e}")
            errores_batch += 1

    return valores_batch, errores_batch


def generate_codigos_postales_sql(df: pd.DataFrame) -> Tuple[int, int]:
    """
    Genera el archivo SQL para la tabla 'codigos_postales', procesando en lotes.

    Args:
        df (pd.DataFrame): DataFrame completo con los datos fuente.

    Returns:
        Tuple[int, int]: Tupla con (registros insertados, número de errores).
    """
    filepath = OUTPUT_DIR / "006_insert_codigos_postales.sql"
    required_cols = ["d_codigo", "d_asenta", "c_estado", "c_tipo_asenta"]
    if not all(col in df.columns for col in required_cols):
        logger.error(f"Faltan columnas {required_cols} para generar códigos postales.")
        _write_sql_file(filepath, "codigos_postales", [], [], "códigos postales")
        return 0, len(df)

    total_records = len(df)
    total_inserted = 0
    total_errors = 0
    num_batches = math.ceil(total_records / BATCH_SIZE_CODIGOS_POSTALES)

    columns = [
        "codigo_postal", "nombre_asentamiento", "fk_codigo_estado",
        "fk_codigo_municipio", "fk_codigo_ciudad", "fk_codigo_tipo_asentamiento",
        "fk_id_zona"
    ]

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("BEGIN;\n")
            cols_sql = ", ".join(columns)
            insert_prefix = f"INSERT INTO codigos_postales ({cols_sql}) VALUES\n"
            first_batch = True

            logger.info(f"Procesando {total_records} códigos postales en {num_batches} lotes de tamaño {BATCH_SIZE_CODIGOS_POSTALES}...")

            for i in range(num_batches):
                start_idx = i * BATCH_SIZE_CODIGOS_POSTALES
                end_idx = start_idx + BATCH_SIZE_CODIGOS_POSTALES
                df_batch = df.iloc[start_idx:end_idx]
                logger.debug(f"Procesando lote {i+1}/{num_batches} (índices {start_idx}-{end_idx-1})...")

                valores_batch, errores_batch = _process_cp_batch(df_batch)
                total_errors += errores_batch

                if valores_batch:
                    if first_batch:
                        f.write(insert_prefix)
                        first_batch = False
                    else:
                        f.write(",\n")

                    f.write(",\n".join(valores_batch))
                    total_inserted += len(valores_batch)
                else:
                     logger.debug(f"Lote {i+1}/{num_batches} no generó valores insertables.")

            if total_inserted > 0:
                 f.write(";\n")
                 logger.info(f"Generado SQL para {total_inserted} códigos postales.")
            else:
                 f.write(f"-- No se encontraron códigos postales válidos\n")
                 logger.warning(f"No se encontraron códigos postales válidos para generar {filepath.name}")

            f.write("COMMIT;\n")

        if total_errors > 0:
            logger.warning(f"Se encontraron {total_errors} errores durante el procesamiento de códigos postales.")

        return total_inserted, total_errors

    except IOError:
        logger.exception(f"Error al escribir el archivo SQL {filepath.name}")
        return total_inserted, total_errors + (total_records - total_inserted - total_errors)
    except Exception:
        logger.exception("Error inesperado al generar SQL para códigos postales")
        return total_inserted, total_errors + (total_records - total_inserted - total_errors) 