from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/madrugada")
def madrugada():
    df = pd.read_json("dados/transacoes_treino.json")

    df["hora"] = df["hora"].str[:2].astype(int)

    resultado = df[(df["hora"] >= 0) & (df["hora"] <= 5)]

    return {
        "transacoes_madrugada": len(resultado)
    }