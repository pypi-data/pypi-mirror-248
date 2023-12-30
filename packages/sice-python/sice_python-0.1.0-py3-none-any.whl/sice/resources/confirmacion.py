from pydantic import BaseModel


class ConfirmacionAbono(BaseModel):

    id: str
    mensaje_id: str

    class Config:  # noqa: WPS306, WPS431
        use_enum_values = True

    def build_xml(self):
        """Create an XML from class."""
