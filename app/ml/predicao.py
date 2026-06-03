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


def _score_normalizado(score: float) -> float:
    normalizado = 1 / (1 + math.exp(5 * score))
    return round(normalizado * 100, 1)


def _buscar_historico(conta: str) -> dict:
    try:
        res = requests.get(f'http://localhost:8000/historico/{conta}', timeout=5)
        return res.json()
    except Exception:
        return {"conta": conta, "total": 0, "perfil": None}


def _calcular_desvio_comportamental(transacao: dict, perfil: dict) -> dict:
    desvios = {}

    valor        = transacao.get('valor', 0)
    hora_int     = int(transacao.get('hora', '00:00').split(':')[0])
    tentativas   = transacao.get('tentativas', 1)
    dispositivo  = transacao.get('dispositivo', '')
    cidade       = transacao.get('cidade', '')
    categoria    = transacao.get('categoria', '')

    valor_medio  = perfil.get('valor_medio', 0)
    valor_max    = perfil.get('valor_max', 0)
    hora_media   = perfil.get('hora_media', 12)
    disp_comum   = perfil.get('dispositivo_mais_comum', '')
    cidade_comum = perfil.get('cidade_mais_comum', '')
    cat_comum    = perfil.get('categoria_mais_comum', '')
    total_fraudes = perfil.get('total_fraudes', 0)
    total_transacoes = perfil.get('total', 1)

    if valor_max > 0:
        desvios['valor'] = min(valor / valor_max, 1.0)
    else:
        desvios['valor'] = 0.0

    desvio_hora = abs(hora_int - hora_media)
    desvios['horario'] = min(desvio_hora / 12.0, 1.0)

    desvios['dispositivo'] = 1.0 if (disp_comum and dispositivo != disp_comum) else 0.0
    desvios['cidade'] = 1.0 if (cidade_comum and cidade and cidade != cidade_comum) else 0.0
    desvios['categoria'] = 1.0 if (cat_comum and categoria != cat_comum) else 0.0
    desvios['tentativas'] = min((tentativas - 1) / 3.0, 1.0)
    desvios['historico_fraude'] = min(total_fraudes / max(total_transacoes, 1), 1.0)

    return desvios


def _analisar_com_historico(transacao: dict, historico: dict) -> list:
    motivos = []
    perfil  = historico.get('perfil')

    valor       = transacao.get('valor', 0)
    hora_int    = int(transacao.get('hora', '00:00').split(':')[0])
    tentativas  = transacao.get('tentativas', 1)
    dispositivo = transacao.get('dispositivo', '')
    cidade      = transacao.get('cidade', '')
    categoria   = transacao.get('categoria', '')

    if perfil and historico.get('total', 0) > 0:
        valor_medio   = perfil.get('valor_medio', 0)
        valor_max     = perfil.get('valor_max', 0)
        hora_media    = perfil.get('hora_media', 12)
        disp_comum    = perfil.get('dispositivo_mais_comum', '')
        cidade_comum  = perfil.get('cidade_mais_comum', '')
        cat_comum     = perfil.get('categoria_mais_comum', '')
        total_fraudes = perfil.get('total_fraudes', 0)

        if valor_medio > 0:
            desvio_pct = (valor - valor_medio) / valor_medio * 100
            if desvio_pct > 50:
                motivos.append(
                    f"Valor R$ {valor:.2f} representa desvio de {desvio_pct:.0f}% "
                    f"acima da média histórica desta conta (R$ {valor_medio:.2f})"
                )

        if valor_max > 0 and valor > valor_max:
            motivos.append(
                f"Valor R$ {valor:.2f} ultrapassa o maior valor já registrado "
                f"por esta conta (R$ {valor_max:.2f})"
            )

        desvio_hora = abs(hora_int - hora_media)
        if desvio_hora > 6:
            motivos.append(
                f"Horário {transacao.get('hora')} representa desvio de {desvio_hora:.0f}h "
                f"em relação ao horário habitual desta conta ({hora_media:.0f}h)"
            )

        if disp_comum and dispositivo != disp_comum:
            motivos.append(
                f"Dispositivo '{dispositivo}' não é o habitual desta conta "
                f"(habitualmente usa '{disp_comum}')"
            )

        if cidade_comum and cidade and cidade != cidade_comum:
            motivos.append(
                f"Transação originada em '{cidade}', divergindo da "
                f"localização habitual desta conta ('{cidade_comum}')"
            )

        if cat_comum and categoria != cat_comum:
            motivos.append(
                f"Categoria '{categoria}' é incomum para esta conta "
                f"(padrão histórico: '{cat_comum}')"
            )

        if total_fraudes > 0:
            proporcao = total_fraudes / max(historico.get('total', 1), 1) * 100
            motivos.append(
                f"Esta conta possui {total_fraudes} ocorrência(s) de fraude "
                f"no histórico ({proporcao:.1f}% das transações)"
            )

    else:
        motivos.append("Conta sem histórico — análise baseada em padrões globais do sistema")
        if hora_int >= 0 and hora_int <= 5:
            motivos.append(f"Horário atípico: {transacao.get('hora')} (madrugada)")
        if valor > 3000:
            motivos.append(f"Valor elevado para conta sem histórico: R$ {valor:.2f}")

    if tentativas >= 2:
        motivos.append(
            f"{tentativas} tentativa(s) registradas — "
            f"{'acima do padrão' if tentativas >= 3 else 'atenção'}"
        )

    if not motivos:
        motivos.append("Comportamento dentro do padrão histórico desta conta")

    return motivos


def _recomendar_acao(desvios: dict, is_fraude: bool, historico: dict) -> dict:
    if not is_fraude:
        return {
            "acao": "LIBERAR",
            "descricao": "Comportamento dentro do padrão histórico desta conta",
            "cor": "verde"
        }

    pesos = {
        'valor':            0.20,
        'horario':          0.15,
        'dispositivo':      0.20,
        'cidade':           0.20,
        'categoria':        0.10,
        'tentativas':       0.10,
        'historico_fraude': 0.05,
    }

    score_comportamental = sum(
        desvios.get(k, 0) * v for k, v in pesos.items()
    )

    if score_comportamental >= 0.55:
        return {
            "acao": "BLOQUEAR",
            "descricao": "Múltiplos desvios críticos do perfil histórico desta conta — bloqueio recomendado",
            "cor": "vermelho"
        }
    elif score_comportamental >= 0.30:
        return {
            "acao": "MONITORAR",
            "descricao": "Desvios moderados do perfil histórico — autenticação adicional recomendada",
            "cor": "amarelo"
        }
    else:
        return {
            "acao": "MONITORAR",
            "descricao": "Anomalia detectada pelo modelo — monitorar esta transação",
            "cor": "amarelo"
        }


def _gerar_explicacao(transacao: dict, is_fraude: bool, score: float,
                       nivel_risco: str, confianca: float, motivos: list,
                       recomendacao: dict, historico: dict,
                       desvios: dict) -> str:

    perfil = historico.get('perfil')
    total  = historico.get('total', 0)
    motivos_texto = "\n".join([f"- {m}" for m in motivos])
    desvios_texto = "\n".join([
        f"- {k}: {v*100:.0f}% de desvio" for k, v in desvios.items()
    ])

    contexto_historico = f"""
- Total de transações: {total}
- Valor médio: R$ {perfil.get('valor_medio') if perfil else 'N/A'}
- Valor máximo já registrado: R$ {perfil.get('valor_max') if perfil else 'N/A'}
- Horário médio de uso: {perfil.get('hora_media') if perfil else 'N/A'}h
- Dispositivo habitual: {perfil.get('dispositivo_mais_comum') if perfil else 'N/A'}
- Cidade habitual: {perfil.get('cidade_mais_comum') if perfil else 'N/A'}
- Categoria mais comum: {perfil.get('categoria_mais_comum') if perfil else 'N/A'}
- Fraudes anteriores: {perfil.get('total_fraudes', 0) if perfil else 0}""" if perfil else "Conta sem histórico anterior no sistema."

    prompt = f"""Você é ARIA (Automated Risk Intelligence Analyst), sistema especialista em detecção de fraudes do Banco do Brasil, integrado diretamente ao pipeline de Machine Learning e ao banco de dados transacional em tempo real.

Seu funcionamento segue três etapas obrigatórias antes de emitir qualquer parecer:

ETAPA 1 — MAPEAMENTO DE PERFIL
Examine o histórico completo desta conta e estabeleça o que é "normalidade" para este cliente específico. Considere: faixa de valor habitual, janela de horário típica, dispositivos utilizados, localização geográfica recorrente e categorias de gasto predominantes.

ETAPA 2 — ANÁLISE DE DESVIO CONTEXTUAL
Compare cada dimensão da transação atual com o perfil mapeado. Não aplique regras genéricas — um valor de R$ 5.000 pode ser normal para um cliente e extremamente suspeito para outro. O desvio só é relevante quando rompe o padrão individual desta conta.

ETAPA 3 — CORRELAÇÃO E PARECER
Com base nos desvios reais identificados, formule um diagnóstico comportamental e justifique a recomendação de ação de forma clara para o operador.

---

DADOS DA TRANSAÇÃO ATUAL:
- Conta: {transacao.get('conta', 'desconhecida')}
- Valor: R$ {transacao.get('valor')}
- Horário: {transacao.get('hora')}
- Tentativas: {transacao.get('tentativas')}
- Dispositivo: {transacao.get('dispositivo')}
- Tipo de transação: {transacao.get('tipo_transacao')}
- Categoria: {transacao.get('categoria')}
- Cidade: {transacao.get('cidade', 'não informada')}

PERFIL HISTÓRICO DESTA CONTA NO BANCO DE DADOS:
{contexto_historico}

RESULTADO DO MODELO ISOLATION FOREST:
- Classificação: {'⚠ ANOMALIA DETECTADA' if is_fraude else '✓ DENTRO DO PADRÃO'}
- Score bruto: {score} (negativo = isolamento rápido = anomalia)
- Nível de risco: {nivel_risco}
- Confiança estatística: {confianca}%

GRAU DE DESVIO POR DIMENSÃO (0% = padrão histórico, 100% = desvio máximo):
{desvios_texto}

DESVIOS IDENTIFICADOS EM RELAÇÃO AO PERFIL DESTA CONTA:
{motivos_texto}

AÇÃO RECOMENDADA PELO SISTEMA: {recomendacao['acao']}

---

Com base exclusivamente nos dados históricos reais desta conta e nos desvios identificados acima, emita seu parecer técnico em português. Seu parecer deve:
1. Descrever o comportamento padrão desta conta conforme o histórico
2. Identificar quais aspectos desta transação rompem esse padrão
3. Justificar a recomendação de ação com base nos desvios reais
4. Ser direto e objetivo, sem suposições genéricas

Parecer técnico:"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'llama3.2',
                'prompt': prompt,
                'stream': False
            },
            timeout=60
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
    score_norm   = _score_normalizado(score)
    conta        = transacao.get('conta', '')
    historico    = _buscar_historico(conta) if conta else {"total": 0, "perfil": None}
    perfil       = historico.get('perfil') or {}
    desvios      = _calcular_desvio_comportamental(transacao, perfil)
    motivos      = _analisar_com_historico(transacao, historico)
    recomendacao = _recomendar_acao(desvios, is_fraude, historico)
    explicacao   = _gerar_explicacao(transacao, is_fraude, round(float(score), 4),
                                      nivel_risco, confianca, motivos,
                                      recomendacao, historico, desvios)

    return {
        "is_fraude":         is_fraude,
        "score":             round(float(score), 4),
        "score_normalizado": score_norm,
        "confianca":         confianca,
        "nivel_risco":       nivel_risco,
        "motivos":           motivos,
        "recomendacao":      recomendacao,
        "explicacao":        explicacao
    }