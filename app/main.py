from fastapi import FastAPI

# =========================
# ROTAS PRINCIPAIS
# =========================
from app.routes.transaction import router as transaction_router


# =========================
# ROTAS DE ANÁLISE
# =========================
from app.routes.dispositivo import router as dispositivo_router
from app.routes.tentativas import router as tentativas_router
from app.routes.conta_transacoes import router as conta_router
from app.routes.fraude_horario import router as fraude_router
from app.routes.media_categoria import router as media_router
from app.routes.madrugada import router as madrugada_router
from app.routes.cidade import router as cidade_router
from app.routes.comparacao_dispositivo import router as comp_router
from app.routes.valor_suspeito import router as valor_router


# =========================
# APP FASTAPI
# =========================
app = FastAPI(
    title="Fraud Transactions API"
)

# =========================
# INCLUDE ROUTERS (PRINCIPAL)
# =========================
app.include_router(transaction_router)


app.include_router(dispositivo_router, tags=["Analise"])
app.include_router(tentativas_router, tags=["Analise"])
app.include_router(conta_router, tags=["Analise"])
app.include_router(fraude_router, tags=["Analise"])
app.include_router(media_router, tags=["Analise"])
app.include_router(madrugada_router, tags=["Analise"])
app.include_router(cidade_router, tags=["Analise"])
app.include_router(comp_router, tags=["Analise"])
app.include_router(valor_router, tags=["Analise"])


# =========================
# HOME (opcional)
# =========================
@app.get("/")
def home():
    return {"msg": "API running!"}