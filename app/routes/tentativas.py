from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/tentativas-fraude")
def tentativas_fraude():
    df = pd.read_json("dados/transacoes_treino.json")

    resultado = df.groupby("is_fraude")["tentativas"].mean()

    return {
        "media_tentativas_fraude": float(resultado[1]),
        "media_tentativas_normal": float(resultado[0])
    }