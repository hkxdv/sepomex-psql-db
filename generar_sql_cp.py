import pandas as pd

# Función para limpiar caracteres especiales
def clean_text(text):
    if pd.isna(text):
        return ""
    # Reemplazar caracteres problemáticos
    replacements = {
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "Á": "A",
        "É": "E",
        "Í": "I",
        "Ó": "O",
        "Ú": "U",
        "ñ": "n",
        "Ñ": "N",
        "´": "",
        "`": "",
        "¨": "",
        "°": "",
        "'": "''",  # Escapar comillas simples para SQL
    }
    result = str(text)
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


# Función para asegurar el formato correcto de los códigos
def format_codigo(codigo, digits=2):
    if pd.isna(codigo) or str(codigo).strip() == "" or str(codigo).lower() == "nan":
        return None  # Para valores NULL

    # Eliminar decimales y convertir a entero
    try:
        codigo_int = int(float(str(codigo).strip()))
        return str(codigo_int).zfill(digits)
    except ValueError:
        return None


# Función para verificar y reportar longitudes incorrectas
def verify_length(value, expected_length, field_name):
    if len(str(value)) > expected_length:
        print(
            f"Error de longitud en {field_name}: '{value}' excede {expected_length} caracteres"
        )
        return False
    return True


# Leer el archivo
df = pd.read_csv(
    "sepomex_original_data.txt",
    sep="|",
    encoding="windows-1252",
)

# Verificar total de registros
print(f"\nTotal de registros en archivo original: {len(df)}")

# Limpiar códigos de ciudad
df["c_cve_ciudad"] = df["c_cve_ciudad"].apply(lambda x: format_codigo(x, 2))

# 1. Procesar estados
estados_df = df[["c_estado", "d_estado"]].drop_duplicates()
with open("database/001_insert_estados.sql", "w", encoding="utf-8") as f:
    f.write("INSERT INTO estados (codigo_estado, nombre_estado) VALUES\n")
    valores = [
        f"('{format_codigo(row['c_estado'])}', '{row['d_estado']}')"
        for _, row in estados_df.iterrows()
    ]
    f.write(",\n".join(valores) + ";")

# 2. Procesar municipios
municipios_df = df[["c_mnpio", "c_estado", "D_mnpio"]].drop_duplicates()
with open("database/002_insert_municipios.sql", "w", encoding="utf-8") as f:
    f.write(
        "INSERT INTO municipios (codigo_municipio, codigo_estado, nombre_municipio) VALUES\n"
    )
    valores = [
        f"('{format_codigo(row['c_mnpio'], 3)}', '{format_codigo(row['c_estado'])}', '{row['D_mnpio']}')"
        for _, row in municipios_df.iterrows()
    ]
    f.write(",\n".join(valores) + ";")

# 3. Procesar tipos de asentamiento
tipos_df = df[["c_tipo_asenta", "d_tipo_asenta"]].drop_duplicates()
with open("database/003_insert_tipos_asentamiento.sql", "w", encoding="utf-8") as f:
    f.write(
        "INSERT INTO tipos_asentamiento (codigo_tipo_asentamiento, nombre_tipo_asentamiento) VALUES\n"
    )
    valores = [
        f"('{format_codigo(row['c_tipo_asenta'], 2)}', '{row['d_tipo_asenta']}')"
        for _, row in tipos_df.iterrows()
    ]
    f.write(",\n".join(valores) + ";")

# 4. Procesar zonas
zonas_df = df["d_zona"].drop_duplicates()
with open("database/005_insert_zonas.sql", "w", encoding="utf-8") as f:
    f.write("INSERT INTO zonas (tipo_zona) VALUES\n")
    valores = [f"('{zona}')" for zona in zonas_df]
    f.write(",\n".join(valores) + ";")

# 5. Procesar ciudades antes de códigos postales
ciudades_df = (
    df[["c_cve_ciudad", "c_estado", "d_ciudad"]]
    .dropna(subset=["c_cve_ciudad"])
    .drop_duplicates()
)
with open("database/004_insert_ciudades.sql", "w", encoding="utf-8") as f:
    f.write(
        "INSERT INTO ciudades (codigo_ciudad, codigo_estado, nombre_ciudad) VALUES\n"
    )
    valores = []
    for _, row in ciudades_df.iterrows():
        codigo_ciudad = format_codigo(row["c_cve_ciudad"], 2)
        if codigo_ciudad is not None:  # Solo incluir ciudades con código válido
            valores.append(
                f"('{codigo_ciudad}', "
                f"'{format_codigo(row['c_estado'], 2)}', "
                f"'{clean_text(row['d_ciudad'])}')"
            )
    f.write(",\n".join(valores) + ";")

# 5. Procesar códigos postales
with open("database/006_insert_codigos_postales.sql", "w", encoding="utf-8") as f:
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
    for idx, row in df.iterrows():
        zona_tipo = clean_text(row["d_zona"])
        id_zona = "1" if zona_tipo == "Urbano" else "2" if zona_tipo == "Rural" else "3"

        try:
            valor = f"""(
                '{format_codigo(row['d_codigo'], 5)}',
                '{clean_text(row['d_asenta'])}',
                '{format_codigo(row['c_estado'], 2)}',
                '{format_codigo(row['c_mnpio'], 3)}',
                {('NULL' if row['c_cve_ciudad'] is None else f"'{row['c_cve_ciudad']}'")},
                '{format_codigo(row['c_tipo_asenta'], 2)}',
                {id_zona},
                '{format_codigo(row['d_CP'], 5)}',
                '{format_codigo(row['c_oficina'], 5)}',
                '{format_codigo(row['id_asenta_cpcons'], 4)}'
            )"""
            valores.append(valor)
        except Exception as e:
            print(f"Error en fila {idx}: {e}")
            print(f"Datos: {row.to_dict()}")

    f.write(",\n".join(valores) + ";")
