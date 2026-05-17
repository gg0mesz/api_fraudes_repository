from fastapi import APIRouter
import pandas as pd

router = APIRouter(prefix="/analise", tags=["Analises"])

@router.get("/fraude-horario")
def fraude_horario():
    df = pd.read_json("dados/transacoes_treino.json")

    df["hora"] = df["hora"].str[:2].astype(int)

    resultado = df.groupby("hora")["is_fraude"].sum().sort_values(ascending=False)

    return {
        "hora_mais_fraude": int(resultado.index[0]),
        "total_fraudes": int(resultado.values[0])
    }