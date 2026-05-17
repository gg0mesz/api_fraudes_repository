from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/valor-suspeito")
def valor_suspeito():
    df = pd.read_json("dados/transacoes_treino.json")

    media = df.groupby("categoria")["valor"].transform("mean")

    df["valor_suspeito"] = df["valor"] > 2 * media

    return {
        "total_suspeitos": int(df["valor_suspeito"].sum())
    }