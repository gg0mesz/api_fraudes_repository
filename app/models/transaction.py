from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Transaction(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Float)
    data = Column(String)
    hora = Column(String)
    dia_semana = Column(String)
    categoria = Column(String)
    conta = Column(String)
    cidade = Column(String)
    estado = Column(String)
    pais = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    tipo_transacao = Column(String)
    dispositivo = Column(String)
    estabelecimento = Column(String)
    tentativas = Column(Integer)
    ip_origem = Column(String)
    is_fraude = Column(Integer)