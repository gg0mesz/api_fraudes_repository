from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionSchema
from app.services.anomalies import detect_anomalies

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def home():
    return {"msg": "API running!"}

@router.get("/transactions")
def list_transactions(
    categoria: str | None = None,
    cidade: str | None = None,
    valor_min: float | None = None,
    valor_max: float | None = None,
    tipo_transacao: str | None = None,
    dispositivo: str | None = None,
    data: str | None = None,
    is_fraude: int | None = Query(default=None, ge=0, le=1),
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)

    if categoria:
        query = query.filter(Transaction.categoria == categoria)
    if cidade:
        query = query.filter(Transaction.cidade == cidade)
    if valor_min is not None:
        query = query.filter(Transaction.valor >= valor_min)
    if valor_max is not None:
        query = query.filter(Transaction.valor <= valor_max)
    if tipo_transacao:
        query = query.filter(Transaction.tipo_transacao == tipo_transacao)
    if dispositivo:
        query = query.filter(Transaction.dispositivo == dispositivo)
    if data:
        query = query.filter(Transaction.data == data)
    if is_fraude is not None:
        query = query.filter(Transaction.is_fraude == is_fraude)

    return query.all()

@router.get("/transactions/{id}")
def get_transaction_by_id(id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/transactions")
def create_transaction(transaction: TransactionSchema, db: Session = Depends(get_db)):
    existing = db.query(Transaction).filter(Transaction.id == transaction.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="ID already exists")

    new_transaction = Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.put("/transactions/{id}")
def update_transaction(id: int, data: TransactionSchema, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in data.dict().items():
        setattr(transaction, key, value)

    db.commit()
    db.refresh(transaction)
    return transaction

@router.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@router.get("/anomalies")
def get_anomalies(db: Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    return detect_anomalies(transactions)