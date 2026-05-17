from datetime import timedelta

def hour_to_seconds(hora):
    if hora is None:
        return 0

    if isinstance(hora, timedelta):
        return int(hora.total_seconds())

    if isinstance(hora, (int, float)):
        return int(hora)

    if isinstance(hora, str):
        parts = hora.split(":")
        if len(parts) >= 2:
            h = int(parts[0])
            m = int(parts[1])
            s = int(parts[2]) if len(parts) > 2 else 0
            return h * 3600 + m * 60 + s

    return 0


def detect_anomalies(transactions):
    suspicious = []

    for t in transactions:
        reasons = []

        if t.valor is not None and t.valor > 3000:
            reasons.append("high value")

        seconds = hour_to_seconds(t.hora)
        if 0 <= seconds <= 5 * 3600 + 59 * 60 + 59:
            reasons.append("transaction at dawn")

        if t.tentativas is not None and t.tentativas > 2:
            reasons.append("too many attempts")

        if reasons:
            suspicious.append({
                "id": t.id,
                "valor": t.valor,
                "cidade": t.cidade,
                "tipo_transacao": t.tipo_transacao,
                "reasons": reasons
            })

    return suspicious