#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para la generación de archivos SQL con datos de códigos postales de SEPOMEX.
Procesa datos de un archivo CSV/TXT y genera scripts SQL para la inserción de datos
en una base de datos PostgreSQL.
"""

import os
import re
import pandas as pd


def clean_text(text):
    """
    Limpia el texto conservando caracteres especiales como acentos y eñes.
    Solo escapa caracteres problemáticos para SQL.

    Args:
        text: Texto a limpiar

    Returns:
        Texto limpio
    """
    if pd.isna(text) or text is None:
        return ""

    # Solo escapar caracteres problemáticos para SQL
    replacements = {
        "'": "''",  # Escapar comillas simples para SQL
        '"': '""',  # Escapar comillas dobles
        "\\": "/",  # Reemplazar barras invertidas
    }

    # Convertir a string y normalizar espacios
    result = str(text).strip()
    for old, new in replacements.items():
        result = result.replace(old, new)

    # Eliminar espacios múltiples pero mantener caracteres especiales
    result = " ".join(result.split())

    return result


def format_codigo(codigo, digits=2):
    """
    Formatea códigos numéricos asegurando que tengan el formato correcto y la longitud esperada.

    Args:
        codigo: Código a formatear
        digits: Número de dígitos esperados (rellena con ceros a la izquierda)

    Returns:
        Código formateado o None si es inválido
    """
    if (
        pd.isna(codigo)
        or codigo is None
        or str(codigo).strip() == ""
        or str(codigo).lower() == "nan"
    ):
        return None

    try:
        codigo_str = str(codigo).strip()
        # Manejar casos con punto decimal
        if "." in codigo_str:
            codigo_int = int(float(codigo_str))
        else:
            codigo_int = int(codigo_str)

        # Validar que sea positivo
        if codigo_int < 0:
            print(f"Error: código '{codigo}' es negativo")
            return None

        return str(codigo_int).zfill(digits)
    except (ValueError, TypeError):
        print(f"Error al formatear código: '{codigo}' no se pudo convertir a entero")
        return None


def verify_length(value, expected_length, field_name):
    """
    Verifica que un valor no exceda la longitud máxima esperada.

    Args:
        value: Valor a verificar
        expected_length: Longitud máxima esperada
        field_name: Nombre del campo (para mensajes de error)

    Returns:
        True si es válido, False si excede la longitud
    """
    if value is None:
        return True

    if len(str(value)) > expected_length:
        print(
            f"Error de longitud en {field_name}: '{value}' excede {expected_length} caracteres"
        )
        return False
    return True


def validate_record(row, idx):
    """
    Valida un registro completo verificando todos los campos requeridos.

    Args:
        row: Fila del DataFrame a validar
        idx: Índice de la fila (para mensajes de error)

    Returns:
        True si el registro es válido, False si hay errores
    """
    valid = True
    required_fields = [
        ("d_codigo", 5, "código postal"),
        ("d_asenta", 100, "asentamiento"),
        ("c_estado", 2, "estado"),
        ("c_mnpio", 3, "municipio"),
        ("c_tipo_asenta", 2, "tipo de asentamiento"),
        ("d_CP", 5, "código postal admin"),
        ("c_oficina", 5, "oficina postal"),
        ("id_asenta_cpcons", 4, "ID asentamiento"),
    ]

    for field, length, name in required_fields:
        if field in row and not pd.isna(row[field]):
            formatted_value = (
                format_codigo(row[field], length)
                if field != "d_asenta"
                else clean_text(row[field])
            )
            valid = valid and verify_length(formatted_value, length, name)
        else:
            if field not in ["c_cve_ciudad"]:  # La ciudad puede ser nula
                print(f"Error en fila {idx}: Campo {field} ({name}) está vacío o nulo")
                valid = False

    return valid


def normalize_zona(zona_texto):
    """
    Normaliza los tipos de zona según el esquema de la base de datos.

    Args:
        zona_texto: Texto que representa la zona

    Returns:
        Tipo de zona normalizado (Urbano, Rural o Semiurbano)
    """
    zona_limpia = clean_text(zona_texto).strip().title()

    # Mapeo según restricción CHECK del esquema
    if zona_limpia == "Urbano" or zona_limpia == "Ciudad":
        return "Urbano"
    elif zona_limpia == "Rural":
        return "Rural"
    else:
        return "Semiurbano"  # Valor por defecto para casos no específicos


def process_estados(df, output_dir):
    """
    Genera el SQL para insertar datos de estados.

    Args:
        df: DataFrame con los datos
        output_dir: Directorio de salida

    Returns:
        Número de registros procesados
    """
    try:
        if "c_estado" in df.columns and "d_estado" in df.columns:
            estados_df = df[["c_estado", "d_estado"]].drop_duplicates()
            filepath = os.path.join(output_dir, "001_insert_estados.sql")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("INSERT INTO estados (codigo_estado, nombre_estado) VALUES\n")
                valores = []

                for _, row in estados_df.iterrows():
                    codigo = format_codigo(row["c_estado"], 2)
                    if codigo is not None and re.match(r"^[0-9]{2}$", codigo):
                        valores.append(f"('{codigo}', '{clean_text(row['d_estado'])}')")

                if valores:
                    f.write(",\n".join(valores) + ";")
                    print(f"Generado SQL para {len(valores)} estados")
                    return len(valores)
                else:
                    f.write("-- No se encontraron estados válidos")
                    print("Advertencia: No se encontraron estados válidos")
                    return 0
        else:
            print("Error: No se pudo procesar estados. Faltan columnas requeridas.")
            return 0
    except Exception as e:
        print(f"Error al procesar estados: {e}")
        return 0


def process_municipios(df, output_dir):
    """
    Genera el SQL para insertar datos de municipios.

    Args:
        df: DataFrame con los datos
        output_dir: Directorio de salida

    Returns:
        Número de registros procesados
    """
    try:
        if (
            "c_mnpio" in df.columns
            and "c_estado" in df.columns
            and "D_mnpio" in df.columns
        ):
            municipios_df = df[["c_mnpio", "c_estado", "D_mnpio"]].drop_duplicates()
            filepath = os.path.join(output_dir, "002_insert_municipios.sql")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(
                    "INSERT INTO municipios (codigo_municipio, codigo_estado, nombre_municipio) VALUES\n"
                )
                valores = []

                for _, row in municipios_df.iterrows():
                    codigo_mnpio = format_codigo(row["c_mnpio"], 3)
                    codigo_estado = format_codigo(row["c_estado"], 2)
                    if (
                        codigo_mnpio is not None
                        and codigo_estado is not None
                        and re.match(r"^[0-9]{3}$", codigo_mnpio)
                        and re.match(r"^[0-9]{2}$", codigo_estado)
                    ):
                        valores.append(
                            f"('{codigo_mnpio}', '{codigo_estado}', '{clean_text(row['D_mnpio'])}')"
                        )

                if valores:
                    f.write(",\n".join(valores) + ";")
                    print(f"Generado SQL para {len(valores)} municipios")
                    return len(valores)
                else:
                    f.write("-- No se encontraron municipios válidos")
                    print("Advertencia: No se encontraron municipios válidos")
                    return 0
        else:
            print("Error: No se pudo procesar municipios. Faltan columnas requeridas.")
            return 0
    except Exception as e:
        print(f"Error al procesar municipios: {e}")
        return 0


def process_tipos_asentamiento(df, output_dir):
    """
    Genera el SQL para insertar datos de tipos de asentamiento.

    Args:
        df: DataFrame con los datos
        output_dir: Directorio de salida

    Returns:
        Número de registros procesados
    """
    try:
        if "c_tipo_asenta" in df.columns and "d_tipo_asenta" in df.columns:
            tipos_df = df[["c_tipo_asenta", "d_tipo_asenta"]].drop_duplicates()
            filepath = os.path.join(output_dir, "003_insert_tipos_asentamiento.sql")

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(
                    "INSERT INTO tipos_asentamiento (codigo_tipo_asentamiento, nombre_tipo_asentamiento) VALUES\n"
                )
                valores = []

                for _, row in tipos_df.iterrows():
                    codigo = format_codigo(row["c_tipo_asenta"], 2)
                    if codigo is not None and re.match(r"^[0-9]{2}$", codigo):
                        valores.append(
                            f"('{codigo}', '{clean_text(row['d_tipo_asenta'])}')"
                        )

                if valores:
                    f.write(",\n".join(valores) + ";")
                    print(f"Generado SQL para {len(valores)} tipos de asentamiento")
                    return len(valores)
                else:
                    f.write("-- No se encontraron tipos de asentamiento válidos")
                    print(
                        "Advertencia: No se encontraron tipos de asentamiento válidos"
                    )
                    return 0
        else:
            print(
                "Error: No se pudo procesar tipos de asentamiento. Faltan columnas requeridas."
            )
            return 0
    except Exception as e:
        print(f"Error al procesar tipos de asentamiento: {e}")
        return 0


def process_zonas(df, output_dir):
    """
    Genera el SQL para insertar datos de zonas.

    Args:
        df: DataFrame con los datos
        output_dir: Directorio de salida

    Returns:
        Número de registros procesados
    """
    try:
        filepath = os.path.join(output_dir, "004_insert_zonas.sql")

        if "d_zona" in df.columns:
            # Según la restricción CHECK del esquema, solo hay 3 valores válidos
            zonas_df = df["d_zona"].apply(normalize_zona).drop_duplicates()

            with open(filepath, "w", encoding="utf-8") as f:
                f.write("INSERT INTO zonas (tipo_zona) VALUES\n")
                valores = []

                for zona in zonas_df:
                    if zona in ["Urbano", "Rural", "Semiurbano"]:
                        valores.append(f"('{zona}')")

                if valores:
                    f.write(",\n".join(valores) + ";")
                    print(f"Generado SQL para {len(valores)} zonas")
                    return len(valores)
                else:
                    f.write("-- No se encontraron zonas válidas")
                    print("Advertencia: No se encontraron zonas válidas")
                    return 0
        else:
            # Generar valores predeterminados si falta la columna
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("INSERT INTO zonas (tipo_zona) VALUES\n")
                f.write("('Urbano'),\n('Rural'),\n('Semiurbano');")
                print(
                    "Generado SQL para 3 zonas predeterminadas (no se encontró columna d_zona)"
                )
                return 3
    except Exception as e:
        print(f"Error al procesar zonas: {e}")
        return 0


def process_ciudades(df, output_dir):
    """
    Genera el SQL para insertar datos de ciudades.

    Args:
        df: DataFrame con los datos
        output_dir: Directorio de salida

    Returns:
        Número de registros procesados
    """
    try:
        filepath = os.path.join(output_dir, "005_insert_ciudades.sql")

        if (
            "c_cve_ciudad" in df.columns
            and "c_estado" in df.columns
            and "d_ciudad" in df.columns
        ):
            ciudades_df = (
                df[["c_cve_ciudad", "c_estado", "d_ciudad"]]
                .dropna(subset=["c_cve_ciudad"])
                .drop_duplicates()
            )

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(
                    "INSERT INTO ciudades (codigo_ciudad, codigo_estado, nombre_ciudad) VALUES\n"
                )
                valores = []

                for _, row in ciudades_df.iterrows():
                    codigo_ciudad = format_codigo(row["c_cve_ciudad"], 2)
                    codigo_estado = format_codigo(row["c_estado"], 2)
                    if (
                        codigo_ciudad is not None
                        and codigo_estado is not None
                        and re.match(r"^[0-9]{2}$", codigo_ciudad)
                        and re.match(r"^[0-9]{2}$", codigo_estado)
                    ):
                        valores.append(
                            f"('{codigo_ciudad}', '{codigo_estado}', '{clean_text(row['d_ciudad'])}')"
                        )

                if valores:
                    f.write(",\n".join(valores) + ";")
                    print(f"Generado SQL para {len(valores)} ciudades")
                    return len(valores)
                else:
                    f.write("-- No se encontraron ciudades válidas")
                    print("Advertencia: No se encontraron ciudades válidas")
                    return 0
        else:
            print(
                "Advertencia: No se pudo procesar ciudades. Faltan columnas requeridas."
            )
            # Crear un archivo vacío
            with open(filepath, "w", encoding="utf-8") as f:
                f.write("-- No se encontraron datos de ciudades\n")
            return 0
    except Exception as e:
        print(f"Error al procesar ciudades: {e}")
        return 0


def process_codigos_postales(df, output_dir):
    """
    Genera el SQL para insertar datos de códigos postales.

    Args:
        df: DataFrame con los datos
        output_dir: Directorio de salida

    Returns:
        Tupla (registros procesados, errores)
    """
    try:
        filepath = os.path.join(output_dir, "006_insert_codigos_postales.sql")
        columnas_requeridas = [
            "d_codigo",
            "d_asenta",
            "c_estado",
            "c_mnpio",
            "c_tipo_asenta",
            "d_CP",
            "c_oficina",
            "id_asenta_cpcons",
        ]
        columnas_faltantes = [
            col for col in columnas_requeridas if col not in df.columns
        ]

        if not columnas_faltantes:
            with open(filepath, "w", encoding="utf-8") as f:
                # id_codigo_postal es SERIAL, no se incluye en la inserción
                f.write(
                    """INSERT INTO codigos_postales (
    codigo_postal,
    nombre_asentamiento,
    codigo_estado,
    codigo_municipio,
    codigo_ciudad,
    codigo_tipo_asentamiento,
    id_zona,
    codigo_postal_administracion,
    codigo_oficina_postal,
    id_asentamiento_consecutivo
) VALUES\n"""
                )

                valores = []
                errores = 0

                # Mapeo de zonas a IDs (debe coincidir con los IDs generados en zonas)
                zona_ids = {"Urbano": 1, "Rural": 2, "Semiurbano": 3}

                for idx, row in df.iterrows():
                    zona_tipo = normalize_zona(
                        row["d_zona"] if "d_zona" in df.columns else "Semiurbano"
                    )
                    id_zona = zona_ids.get(zona_tipo, "NULL")

                    try:
                        # Verificar y formatear cada campo según requisitos del schema
                        codigo_postal = format_codigo(row["d_codigo"], 5)
                        codigo_estado = format_codigo(row["c_estado"], 2)
                        codigo_municipio = format_codigo(row["c_mnpio"], 3)
                        codigo_tipo_asenta = format_codigo(row["c_tipo_asenta"], 2)
                        codigo_postal_admin = format_codigo(row["d_CP"], 5)
                        codigo_oficina = format_codigo(row["c_oficina"], 5)
                        id_asenta_cpcons = format_codigo(row["id_asenta_cpcons"], 4)

                        # Verificar que todos los campos obligatorios existan y cumplan con el regex
                        if (
                            codigo_postal is None
                            or codigo_estado is None
                            or codigo_municipio is None
                            or codigo_tipo_asenta is None
                            or codigo_postal_admin is None
                            or id_asenta_cpcons is None
                            or not re.match(r"^[0-9]{5}$", codigo_postal)
                            or not re.match(r"^[0-9]{2}$", codigo_estado)
                            or not re.match(r"^[0-9]{3}$", codigo_municipio)
                            or not re.match(r"^[0-9]{2}$", codigo_tipo_asenta)
                            or not re.match(r"^[0-9]{5}$", codigo_postal_admin)
                            or (
                                codigo_oficina is not None
                                and not re.match(r"^[0-9]{5}$", codigo_oficina)
                            )
                            or not re.match(r"^[0-9]{4}$", id_asenta_cpcons)
                        ):
                            errores += 1
                            continue

                        # Formatear campo de ciudad (puede ser NULL)
                        if (
                            "c_cve_ciudad" not in df.columns
                            or row["c_cve_ciudad"] is None
                            or row["c_cve_ciudad"] == ""
                        ):
                            ciudad_valor = "NULL"
                        else:
                            if re.match(r"^[0-9]{2}$", row["c_cve_ciudad"]):
                                ciudad_valor = f"'{row['c_cve_ciudad']}'"
                            else:
                                ciudad_valor = "NULL"

                        # Formatear campo de oficina postal (puede ser NULL según schema)
                        oficina_valor = (
                            "NULL" if codigo_oficina is None else f"'{codigo_oficina}'"
                        )

                        valor = f"""(
    '{codigo_postal}',
    '{clean_text(row['d_asenta'])}',
    '{codigo_estado}',
    '{codigo_municipio}',
    {ciudad_valor},
    '{codigo_tipo_asenta}',
    {id_zona},
    '{codigo_postal_admin}',
    {oficina_valor},
    '{id_asenta_cpcons}'
)"""
                        valores.append(valor)
                    except Exception as e:
                        print(f"Error en fila {idx}: {e}")
                        if idx < 5:  # Solo mostrar los primeros errores para no saturar
                            print(f"Datos: {row.to_dict()}")
                        errores += 1

                if valores:
                    f.write(",\n".join(valores) + ";")
                    print(f"Generado SQL para {len(valores)} códigos postales")
                else:
                    f.write("-- No se encontraron códigos postales válidos")
                    print("Advertencia: No se encontraron códigos postales válidos")

                return len(valores), errores
        else:
            print(
                f"Error: No se pudo procesar códigos postales. Faltan columnas requeridas: {', '.join(columnas_faltantes)}"
            )
            # Crear un archivo vacío
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(
                    f"-- No se pudieron procesar códigos postales. Faltan columnas: {', '.join(columnas_faltantes)}\n"
                )
            return 0, 0
    except Exception as e:
        print(f"Error al procesar códigos postales: {e}")
        return 0, 0


def main():
    """Función principal que ejecuta el proceso completo"""
    # Crear directorio para salida si no existe
    output_dir = "data"
    os.makedirs(output_dir, exist_ok=True)

    # Configuraciones
    input_file = "sepomex_original_data.txt"

    print(f"Iniciando procesamiento del archivo: {input_file}")
    print("-" * 50)

    # Leer el archivo
    try:
        df = pd.read_csv(input_file, sep="|", encoding="windows-1252", low_memory=False)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    # Verificar total de registros
    print(f"Total de registros en archivo original: {len(df)}")

    # Verificar qué columnas existen en el DataFrame
    columnas_esperadas = [
        "d_codigo",
        "d_asenta",
        "c_estado",
        "D_mnpio",
        "c_mnpio",
        "c_tipo_asenta",
        "d_tipo_asenta",
        "c_cve_ciudad",
        "d_ciudad",
        "d_zona",
        "d_CP",
        "c_oficina",
        "id_asenta_cpcons",
    ]
    columnas_faltantes = [col for col in columnas_esperadas if col not in df.columns]

    if columnas_faltantes:
        print(
            f"Advertencia: Las siguientes columnas no están en el archivo: {', '.join(columnas_faltantes)}"
        )
        print("Columnas disponibles:", ", ".join(df.columns))

    # Preprocesar y limpiar datos
    # Rellenar valores nulos solo en columnas que existen
    if "c_cve_ciudad" in df.columns:
        df["c_cve_ciudad"] = df["c_cve_ciudad"].fillna("")

    if "d_zona" in df.columns:
        df["d_zona"] = df["d_zona"].fillna("Semiurbano")

    # Limpiar códigos de ciudad solo si la columna existe
    if "c_cve_ciudad" in df.columns:
        df["c_cve_ciudad"] = df["c_cve_ciudad"].apply(lambda x: format_codigo(x, 2))

    # Limpiar nombres de asentamientos y otros campos de texto
    for col in ["d_asenta", "d_estado", "D_mnpio", "d_ciudad", "d_zona"]:
        if col in df.columns:
            df[col] = df[col].apply(clean_text)

    # Normalizar zonas según schema CHECK (Urbano, Rural, Semiurbano)
    if "d_zona" in df.columns:
        df["d_zona"] = df["d_zona"].apply(normalize_zona)
    else:
        print(
            "Advertencia: Columna 'd_zona' no encontrada. Se usará 'Semiurbano' por defecto."
        )
        df["d_zona"] = "Semiurbano"

    # Validar dataframe completo
    valid_records = 0
    invalid_records = 0

    print("\nValidando registros...")
    for idx, row in df.iterrows():
        if validate_record(row, idx):
            valid_records += 1
        else:
            invalid_records += 1

    print(f"Registros válidos: {valid_records}")
    print(f"Registros con problemas: {invalid_records}")
    print("-" * 50)

    # Procesar y generar archivos SQL
    print("\nGenerando archivos SQL:")
    estados_count = process_estados(df, output_dir)
    municipios_count = process_municipios(df, output_dir)
    tipos_count = process_tipos_asentamiento(df, output_dir)
    zonas_count = process_zonas(df, output_dir)
    ciudades_count = process_ciudades(df, output_dir)
    cp_count, cp_errors = process_codigos_postales(df, output_dir)

    # Resumen final
    print("\n")
    print("-" * 50)
    print(f"Estados procesados: {estados_count}")
    print(f"Municipios procesados: {municipios_count}")
    print(f"Tipos de asentamiento procesados: {tipos_count}")
    print(f"Zonas procesadas: {zonas_count}")
    print(f"Ciudades procesadas: {ciudades_count}")
    print(f"Códigos postales procesados: {cp_count}")
    print(f"Errores en códigos postales: {cp_errors}")
    print("-" * 50)
    print(f"Proceso completado. Archivos SQL generados en el directorio '{output_dir}/'")


if __name__ == "__main__":
    main()
