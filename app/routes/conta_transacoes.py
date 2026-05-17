from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/conta-mais-transacoes")
def conta_mais_transacoes():
    df = pd.read_json("dados/transacoes_treino.json")

    resultado = df["conta"].value_counts().head(1)

    return {
        "conta": resultado.index[0],
        "total_transacoes": int(resultado.values[0])
    }