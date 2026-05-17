from pydantic import BaseModel, Field

class TransactionSchema(BaseModel):
    id: int
    valor: float = Field(gt=0)
    data: str
    hora: str
    dia_semana: str
    categoria: str
    conta: str
    cidade: str
    estado: str
    pais: str
    latitude: float
    longitude: float
    tipo_transacao: str
    dispositivo: str
    estabelecimento: str
    tentativas: int = Field(ge=0)
    ip_origem: str
    is_fraude: int = Field(ge=0, le=1)