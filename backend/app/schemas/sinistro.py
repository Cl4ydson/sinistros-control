from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class SinistroOut(BaseModel):
    id: int
    nr_conhecimento: str | None = None
    cliente: str | None = None
    data_evento: date | None = None
    modal: str | None = None
    tipo_ocorrencia: str | None = None
    valor_mercadoria: Decimal | None = None
    status: str | None = None

    class Config:
        orm_mode = True