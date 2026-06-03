from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.transaction import Transaction

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hora_para_int(hora):
    try:
        if hasattr(hora, 'seconds'):
            return hora.seconds // 3600
        return int(str(hora).split(':')[0])
    except:
        return 12


@router.get("/historico/{conta}", tags=["ML - Deteccao de Fraude"])
def get_historico(conta: str, db: Session = Depends(get_db)):
    transacoes = db.query(Transaction).filter(Transaction.conta == conta).all()

    if not transacoes:
        return {"conta": conta, "total": 0, "perfil": None}

    valores      = [t.valor for t in transacoes if t.valor]
    horas        = [hora_para_int(t.hora) for t in transacoes if t.hora]
    categorias   = [t.categoria for t in transacoes if t.categoria]
    dispositivos = [t.dispositivo for t in transacoes if t.dispositivo]
    cidades      = [t.cidade for t in transacoes if t.cidade]

    return {
        "conta": conta,
        "total": len(transacoes),
        "perfil": {
            "valor_medio":            round(sum(valores) / len(valores), 2) if valores else 0,
            "valor_max":              max(valores) if valores else 0,
            "valor_min":              min(valores) if valores else 0,
            "hora_media":             round(sum(horas) / len(horas), 1) if horas else 0,
            "categoria_mais_comum":   max(set(categorias), key=categorias.count) if categorias else None,
            "dispositivo_mais_comum": max(set(dispositivos), key=dispositivos.count) if dispositivos else None,
            "cidade_mais_comum":      max(set(cidades), key=cidades.count) if cidades else None,
            "total_fraudes":          sum(1 for t in transacoes if t.is_fraude == 1),
        }
    }