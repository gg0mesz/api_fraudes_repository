from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/dispositivo-influencia")
def dispositivo_influencia():
    df = pd.read_json("dados/transacoes_treino.json")

    resultado = (
        df.groupby("dispositivo")["is_fraude"]
        .mean()
        .sort_values(ascending=False)
    )

    return {
        "dispositivo_mais_suspeito": resultado.index[0],
        "taxa_fraude": float(resultado.values[0])
    }