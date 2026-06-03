from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.ml.predicao import prever_fraude

router = APIRouter()


class TransacaoInput(BaseModel):
    conta: str = ""
    valor: float
    hora: str
    tentativas: int
    latitude: float
    longitude: float
    cidade: str = ""
    dispositivo: str
    tipo_transacao: str
    categoria: str


class Recomendacao(BaseModel):
    acao: str
    descricao: str
    cor: str


class PredicaoOutput(BaseModel):
    is_fraude: bool
    score: float
    score_normalizado: float
    confianca: float
    nivel_risco: str
    motivos: List[str]
    recomendacao: Recomendacao
    explicacao: str


@router.post(
    "/analisar",
    response_model=PredicaoOutput,
    summary="Analisa se uma transação é suspeita"
)
def analisar_transacao(transacao: TransacaoInput):
    try:
        return prever_fraude(transacao.model_dump())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))