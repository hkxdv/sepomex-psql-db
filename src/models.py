from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Estado:
    """Representa un registro de la tabla 'estados'."""
    pk_codigo_estado: str
    nombre_estado: str


@dataclass(frozen=True)
class Municipio:
    """Representa un registro de la tabla 'municipios'."""
    pk_codigo_municipio: str
    fk_codigo_estado: str
    nombre_municipio: str


@dataclass(frozen=True)
class Ciudad:
    """Representa un registro de la tabla 'ciudades'."""
    pk_codigo_ciudad: str
    fk_codigo_estado: str
    nombre_ciudad: str


@dataclass(frozen=True)
class TipoAsentamiento:
    """Representa un registro de la tabla 'tipos_asentamiento'."""
    pk_codigo_tipo_asentamiento: str
    nombre_tipo_asentamiento: str


@dataclass(frozen=True)
class Zona:
    """Representa un registro de la tabla 'zonas'."""
    pk_id_zona: int
    nombre_zona: str


@dataclass(frozen=True)
class CodigoPostal:
    """Representa un registro de la tabla 'codigos_postales'."""
    codigo_postal: str
    nombre_asentamiento: str
    fk_codigo_estado: str
    fk_codigo_municipio: Optional[str]
    fk_codigo_ciudad: Optional[str]
    fk_codigo_tipo_asentamiento: str
    fk_id_zona: int 