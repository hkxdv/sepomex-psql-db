from pathlib import Path

# Rutas principales (relativas a la raíz del proyecto)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "generated_sql_v2"
LOG_DIR = BASE_DIR / "logs"

# Asegurarse de que los directorios de salida y logs existan
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configuración del archivo de entrada
INPUT_FILENAME = "sepomex_data.txt"
INPUT_FILE_PATH = INPUT_DIR / INPUT_FILENAME
FILE_ENCODING = "windows-1252"
FILE_SEPARATOR = "|"

# Columnas necesarias del archivo de entrada para v2
INPUT_COLUMNS_V2 = [
    'd_codigo', 'd_asenta', 'd_tipo_asenta', 'D_mnpio', 'd_estado',
    'd_ciudad', 'c_estado', 'c_mnpio', 'c_tipo_asenta', 'c_cve_ciudad',
    'd_zona'
]

# Mapeo de zonas (nombre normalizado a ID de la DB v2)
ZONAS_MAP: dict[str, int] = {"Urbano": 1, "Rural": 2, "Semiurbano": 3}
DEFAULT_ZONA_ID: int = ZONAS_MAP["Semiurbano"]
DEFAULT_ZONA_NAME: str = "Semiurbano"

# Configuración de logging
LOG_FILE = LOG_DIR / "sepomex_generator.log"
LOG_LEVEL = "DEBUG"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configuración de procesamiento
BATCH_SIZE_CODIGOS_POSTALES = 10000

# Longitudes máximas permitidas por el esquema v2 (para validación)
MAX_LEN_NOMBRE = 50
MAX_LEN_NOMBRE_ASENTAMIENTO = 100

# Formatos Regex para códigos (según esquema v2)
REGEX_CODIGO_POSTAL = r"^[0-9]{5}$"
REGEX_CODIGO_ESTADO = r"^[0-9]{2}$"
REGEX_CODIGO_MUNICIPIO = r"^[0-9]{3}$"
REGEX_CODIGO_CIUDAD = r"^[0-9]{2}$"
REGEX_CODIGO_TIPO_ASENTA = r"^[0-9]{2}$" 