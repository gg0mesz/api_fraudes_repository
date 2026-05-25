import pickle
import numpy as np
import requests
from pathlib import Path

_MODELO_PATH = Path(__file__).parent / 'modelo.pkl'

with open(_MODELO_PATH, 'rb') as f:
    _artefato = pickle.load(f)

_modelo   = _artefato['modelo']
_encoders = _artefato['encoders']
_features = _artefato['features']


def _gerar_explicacao(transacao: dict, is_fraude: bool, score: float, nivel_risco: str) -> str:
    prompt = f"""Você é um analista de fraudes bancárias. Analise a transação abaixo e explique em 2-3 frases em português se ela é suspeita ou não, e por quê.

Dados da transação:
- Valor: R$ {transacao.get('valor')}
- Horário: {transacao.get('hora')}
- Tentativas: {transacao.get('tentativas')}
- Dispositivo: {transacao.get('dispositivo')}
- Tipo: {transacao.get('tipo_transacao')}
- Categoria: {transacao.get('categoria')}
- Cidade: {transacao.get('cidade', 'não informada')}

Resultado do modelo: {'FRAUDE DETECTADA' if is_fraude else 'TRANSAÇÃO NORMAL'}
Nível de risco: {nivel_risco}
Score: {score}

Responda de forma direta e objetiva."""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2',
                'prompt': prompt,
                'stream': False
            },
            timeout=30
        )
        return response.json().get('response', 'Explicação não disponível.')
    except Exception:
        return 'Serviço de explicação indisponível no momento.'


def prever_fraude(transacao: dict) -> dict:
    hora_int = int(transacao.get('hora', '00:00').split(':')[0])

    def encode(col, valor):
        le = _encoders[col]
        if valor in le.classes_:
            return le.transform([valor])[0]
        return 0

    row = np.array([[
        transacao.get('valor', 0),
        hora_int,
        transacao.get('tentativas', 1),
        transacao.get('latitude', 0),
        transacao.get('longitude', 0),
        encode('dispositivo',    transacao.get('dispositivo', '')),
        encode('tipo_transacao', transacao.get('tipo_transacao', '')),
        encode('categoria',      transacao.get('categoria', '')),
    ]])

    predicao  = _modelo.predict(row)[0]
    score     = _modelo.decision_function(row)[0]
    is_fraude = predicao == -1

    if score < -0.15:
        nivel_risco = "ALTO"
    elif score < 0:
        nivel_risco = "MEDIO"
    else:
        nivel_risco = "BAIXO"

    explicacao = _gerar_explicacao(transacao, is_fraude, round(float(score), 4), nivel_risco)

    return {
        "is_fraude":   is_fraude,
        "score":       round(float(score), 4),
        "nivel_risco": nivel_risco,
        "explicacao":  explicacao
    }