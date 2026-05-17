from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/media-categoria")
def media_categoria():
    df = pd.read_json("dados/transacoes_treino.json")

    resultado = df.groupby("categoria")["valor"].mean().to_dict()

    return resultado