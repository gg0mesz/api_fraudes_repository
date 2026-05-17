from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/comparacao-dispositivo")
def comparacao():
    df = pd.read_json("dados/transacoes_treino.json")

    resultado = df.groupby("dispositivo")["valor"].mean().to_dict()

    return resultado