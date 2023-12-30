from pydantic import BaseModel

from sice.types import CodigoError


class Acuse(BaseModel):
    codigo: CodigoError
    description: str

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True


class Respuesta(BaseModel):
    id: str
    mensaje_id: str
    fecha_oper: int
    resultado_cep: Acuse
    resultado_banxico: Acuse

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True

    @classmethod
    def parse_xml(cls):
        """Build Respuesta from XML."""
