from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ml.predicao import prever_fraude

router = APIRouter()

class TransacaoInput(BaseModel):
    valor: float
    hora: str
    tentativas: int
    latitude: float
    longitude: float
    dispositivo: str
    tipo_transacao: str
    categoria: str

class PredicaoOutput(BaseModel):
    is_fraude: bool
    score: float
    nivel_risco: str
    explicacao: str

@router.post("/analisar", response_model=PredicaoOutput, summary="Analisa se uma transação é suspeita")
def analisar_transacao(transacao: TransacaoInput):
    try:
        return prever_fraude(transacao.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))