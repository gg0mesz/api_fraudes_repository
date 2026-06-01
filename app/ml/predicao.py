import pickle
import numpy as np
import requests
import math
from pathlib import Path

_MODELO_PATH = Path(__file__).parent / 'modelo.pkl'

with open(_MODELO_PATH, 'rb') as f:
    _artefato = pickle.load(f)

_modelo   = _artefato['modelo']
_encoders = _artefato['encoders']
_features = _artefato['features']


def _calcular_confianca(score: float) -> float:
    confianca = 1 / (1 + math.exp(5 * score))
    return round(confianca * 100, 1)


def _analisar_features(transacao: dict) -> list:
    motivos = []
    valor       = transacao.get('valor', 0)
    hora_int    = int(transacao.get('hora', '00:00').split(':')[0])
    tentativas  = transacao.get('tentativas', 1)
    dispositivo = transacao.get('dispositivo', '')
    tipo        = transacao.get('tipo_transacao', '')
    categoria   = transacao.get('categoria', '')

    if valor > 5000:
        motivos.append(f"Valor elevado: R$ {valor:.2f} acima do padrão")
    elif valor > 2000:
        motivos.append(f"Valor moderadamente alto: R$ {valor:.2f}")

    if 0 <= hora_int <= 5:
        motivos.append(f"Horário atípico: {transacao.get('hora')} (madrugada)")

    if tentativas >= 3:
        motivos.append(f"Múltiplas tentativas: {tentativas} tentativas registradas")

    if categoria == 'eletronicos' and valor > 1000:
        motivos.append("Eletrônicos de alto valor: categoria de risco elevado")

    if tipo == 'transferencia' and hora_int <= 5:
        motivos.append("Transferência na madrugada: padrão suspeito")

    if dispositivo == 'web' and tentativas >= 3:
        motivos.append("Acesso web com múltiplas tentativas: possível ataque automatizado")

    if not motivos:
        motivos.append("Padrão dentro do esperado para esta categoria e horário")

    return motivos


def _recomendar_acao(is_fraude: bool, nivel_risco: str, confianca: float, motivos: list, transacao: dict) -> dict:
    if not is_fraude:
        return {
            "acao": "LIBERAR",
            "descricao": "Transação dentro dos padrões esperados",
            "cor": "verde"
        }

    valor      = transacao.get('valor', 0)
    tentativas = transacao.get('tentativas', 1)

    if valor >= 5000 and tentativas >= 3:
        return {
            "acao": "BLOQUEAR",
            "descricao": "Bloquear transação imediatamente e notificar o cliente",
            "cor": "vermelho"
        }
    elif valor >= 1000 or tentativas >= 3:
        return {
            "acao": "MONITORAR",
            "descricao": "Solicitar autenticação adicional do cliente antes de prosseguir",
            "cor": "amarelo"
        }
    else:
        return {
            "acao": "BLOQUEAR",
            "descricao": "Bloquear transação e acionar equipe de análise",
            "cor": "vermelho"
        }


def _gerar_explicacao(transacao: dict, is_fraude: bool, score: float,
                       nivel_risco: str, confianca: float, motivos: list,
                       recomendacao: dict) -> str:
    motivos_texto = "\n".join([f"- {m}" for m in motivos])

    prompt = f"""Você é um analista sênior de fraudes bancárias. Analise a transação abaixo e forneça um parecer técnico em português em 2-3 frases.

Dados da transação:
- Valor: R$ {transacao.get('valor')}
- Horário: {transacao.get('hora')}
- Tentativas: {transacao.get('tentativas')}
- Dispositivo: {transacao.get('dispositivo')}
- Tipo: {transacao.get('tipo_transacao')}
- Categoria: {transacao.get('categoria')}

Resultado do modelo:
- Classificação: {'FRAUDE DETECTADA' if is_fraude else 'TRANSAÇÃO NORMAL'}
- Nível de risco: {nivel_risco}
- Confiança: {confianca}%
- Ação recomendada: {recomendacao['acao']}

Fatores identificados:
{motivos_texto}

Escreva um parecer técnico direto e objetivo."""

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
        return response.json().get('response', 'Parecer não disponível.')
    except Exception:
        return 'Serviço de IA indisponível no momento.'


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

    confianca    = _calcular_confianca(score)
    motivos      = _analisar_features(transacao)
    recomendacao = _recomendar_acao(is_fraude, nivel_risco, confianca, motivos, transacao)
    explicacao   = _gerar_explicacao(transacao, is_fraude, round(float(score), 4),
                                      nivel_risco, confianca, motivos, recomendacao)

    return {
        "is_fraude":    is_fraude,
        "score":        round(float(score), 4),
        "confianca":    confianca,
        "nivel_risco":  nivel_risco,
        "motivos":      motivos,
        "recomendacao": recomendacao,
        "explicacao":   explicacao
    }