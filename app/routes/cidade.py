from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/cidade-fora-pe")
def cidade_fora_pe():
    df = pd.read_json("dados/transacoes_treino.json")

    df = df[df["estado"] != "PE"]

    resultado = df["cidade"].value_counts().head(1)

    return {
        "cidade": resultado.index[0],
        "ocorrencias": int(resultado.values[0])
    }