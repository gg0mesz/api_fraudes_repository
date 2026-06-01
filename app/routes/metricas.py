from fastapi import APIRouter
from pathlib import Path
import pickle

router = APIRouter()

_MODELO_PATH = Path(__file__).parent.parent / 'ml' / 'modelo.pkl'


@router.get(
    "/ml/metricas",
    tags=["ML - Deteccao de Fraude"],
    summary="Retorna as métricas de desempenho do modelo"
)
def get_metricas():
    with open(_MODELO_PATH, 'rb') as f:
        artefato = pickle.load(f)
    return artefato.get('metricas', {})